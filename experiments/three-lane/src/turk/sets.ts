// The places of story-chess-turk v7 as real 3D sets (our own code): Schönbrunn's courtyard and facade, the palace
// hall (day and night), a Paris salon, a touring map on a table, the Philadelphia museum (street and burning
// gallery) and a night workshop for the explanation. Simple modelled geometry + code-painted textures, re-shaded
// two-tone (shade.ts) so the ink pass, lens blur and grade make them read like lit storybook sets. Every set brings
// its own key light (the only shadow caster); the Stage colours it from the story's light preset.
import * as THREE from "three";
import { twoTone } from "../shade";
import { NOINK } from "../ink";
import { woodFloor, plaster, lacquer } from "../paint";
import { paving, stucco, marbleChecker, panelWall, stoneWall, darkBoards, brass, skyGrad, signTex, glow, tex } from "./paint2";

export const lambert = (p: THREE.MeshLambertMaterialParameters) => twoTone(new THREE.MeshLambertMaterial(p));
const basic = (p: THREE.MeshBasicMaterialParameters) => new THREE.MeshBasicMaterial({ fog: false, ...p });

export type SetBuild = {
  root: THREE.Group;
  key: THREE.DirectionalLight;
  glows: THREE.Object3D[];                       // additive light pools (scaled by the preset's glow amount)
  sky?: THREE.Mesh;
  extra: Record<string, THREE.Object3D>;          // named anchors / animated parts for the story
};

export function makeKey(root: THREE.Group, pos: [number, number, number], target: [number, number, number], span = 9) {
  const key = new THREE.DirectionalLight("#ffe2b8", 2.0);
  key.position.set(...pos); key.target.position.set(...target);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -span, right: span, top: span, bottom: -span, near: 0.5, far: 60 });
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  root.add(key, key.target);
  return key;
}

function box(root: THREE.Object3D, mat: THREE.Material, w: number, h: number, d: number, x: number, y: number, z: number, cast = true) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat);
  m.position.set(x, y, z); m.castShadow = cast; m.receiveShadow = true;
  root.add(m); return m;
}
function cyl(root: THREE.Object3D, mat: THREE.Material, r: number, h: number, x: number, y: number, z: number, seg = 20) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat);
  m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true;
  root.add(m); return m;
}
function plane(root: THREE.Object3D, mat: THREE.Material, w: number, h: number, x: number, y: number, z: number, rx = 0, ry = 0) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  m.position.set(x, y, z); m.rotation.set(rx, ry, 0); m.receiveShadow = true;
  root.add(m); return m;
}
export function glowSprite(root: THREE.Object3D, rgb: [number, number, number], size: number, x: number, y: number, z: number) {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glow(rgb), blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true }));
  s.scale.set(size, size, 1); s.position.set(x, y, z); s.layers.set(NOINK);
  root.add(s); return s;
}
function skyCard(root: THREE.Object3D, t: THREE.Texture, w: number, h: number, x: number, y: number, z: number, ry = 0) {
  const m = plane(root, basic({ map: t }), w, h, x, y, z, 0, ry);
  m.layers.set(NOINK); return m;
}
function arch(w: number, h: number) {
  const s = new THREE.Shape();
  s.moveTo(-w / 2, 0); s.lineTo(-w / 2, h - w / 2); s.absarc(0, h - w / 2, w / 2, Math.PI, 0, true); s.lineTo(w / 2, 0); s.lineTo(-w / 2, 0);
  return new THREE.ShapeGeometry(s, 16);
}

// ------------------------------------------------------------------------------------------------ Schönbrunn courtyard
export function exteriorSet(): SetBuild {
  const root = new THREE.Group();
  const ground = plane(root, lambert({ map: paving([10, 10]) }), 80, 80, 0, 0, -10, -Math.PI / 2);
  ground.receiveShadow = true;
  const wall = lambert({ map: stucco([4, 2]) });
  const white = lambert({ color: "#f2ead8" });
  const roof = lambert({ color: "#6f7790" });
  const glass = lambert({ color: "#3d5a86" });
  // main block, centre pavilion, wings coming forward
  box(root, wall, 34, 11, 3, 0, 5.5, -22);
  box(root, roof, 34.4, 1.2, 3.4, 0, 11.6, -22);
  box(root, wall, 10, 14, 3, 0, 7, -20);
  const ped = new THREE.Shape(); ped.moveTo(-5.6, 0); ped.lineTo(5.6, 0); ped.lineTo(0, 2.6); ped.lineTo(-5.6, 0);
  const pedM = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 0.8, bevelEnabled: false }), white);
  pedM.position.set(0, 14, -18.9); pedM.castShadow = true; root.add(pedM);
  for (let i = 0; i < 6; i++) cyl(root, white, 0.42, 10, -3.75 + i * 1.5, 5, -18.2);
  box(root, white, 10.4, 0.7, 1.4, 0, 10.35, -18.4);
  for (const side of [-1, 1]) {
    box(root, wall, 4, 10, 18, side * 15, 5, -12);
    box(root, roof, 4.4, 1, 18.4, side * 15, 10.5, -12);
    for (let k = 0; k < 5; k++) for (let row = 0; row < 2; row++) {
      box(root, white, 0.25, 2.5, 1.5, side * 12.9, 2.4 + row * 4, -18 + k * 3.4);
      box(root, glass, 0.12, 2.1, 1.1, side * 12.8, 2.4 + row * 4, -18 + k * 3.4, false);
    }
  }
  for (let k = 0; k < 9; k++) for (let row = 0; row < 2; row++) {
    const x = -16 + k * 4; if (Math.abs(x) < 5.5) continue;
    box(root, white, 1.6, 2.6, 0.25, x, 2.6 + row * 4.4, -20.4);
    box(root, glass, 1.2, 2.2, 0.12, x, 2.6 + row * 4.4, -20.3, false);
  }
  // arched door
  const door = new THREE.Mesh(arch(2.6, 4.6), lambert({ color: "#2b2440" }));
  door.position.set(0, 0, -18.45); root.add(door);
  // trees and lamp posts for parallax
  const leaf = lambert({ color: "#4f8a4c" }), trunk = lambert({ color: "#6b4a2b" });
  for (const [x, z] of [[-9, -6], [9, -5], [-11, 3], [11, 4], [-7, 9], [7, 10]]) {
    cyl(root, trunk, 0.18, 2.2, x, 1.1, z);
    const s = new THREE.Mesh(new THREE.SphereGeometry(1.6, 18, 14), leaf); s.position.set(x, 3.3, z); s.castShadow = true; root.add(s);
  }
  const iron = lambert({ color: "#2b2b3a" });
  for (const x of [-4.5, 4.5]) for (const z of [-2, 6]) { cyl(root, iron, 0.06, 3.2, x, 1.6, z, 8); box(root, iron, 0.4, 0.5, 0.4, x, 3.35, z); }
  const sky = skyCard(root, skyGrad("#7fa7d6", "#bcd2e6", "#f1dcb4"), 160, 70, 0, 26, -40);
  const key = makeKey(root, [14, 20, 16], [0, 0, -8], 22);
  return { root, key, glows: [], sky, extra: {} };
}

// ------------------------------------------------------------------------------------------------ palace hall
export function hallSet(night: boolean): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  const W = 12, X0 = -6, Z0 = -20, Z1 = 8, H = 7.5;
  plane(root, lambert({ map: woodFloor([5, 9]) }), W, Z1 - Z0, 0, 0, (Z0 + Z1) / 2, -Math.PI / 2);
  // carpet runner
  box(root, lambert({ map: tex(runner(), [1, 6]) }), 2.4, 0.02, Z1 - Z0 - 2, 0, 0.01, (Z0 + Z1) / 2 + 1, false);
  const wallMat = lambert({ map: plaster([3, 1]), color: night ? "#c9c3e6" : "#f3e7f6" });
  const gold = lambert({ map: brass() });
  const lac = lambert({ map: lacquer([1, 2]) });
  box(root, wallMat, W, H, 0.3, 0, H / 2, Z0 - 0.15);                // throne wall
  box(root, wallMat, W, H, 0.3, 0, H / 2, Z1 + 0.15);                // entrance wall
  box(root, wallMat, 0.3, H, Z1 - Z0, X0 - 0.15, H / 2, (Z0 + Z1) / 2);   // window wall (left)
  box(root, wallMat, 0.3, H, Z1 - Z0, -X0 + 0.15, H / 2, (Z0 + Z1) / 2);  // mirror wall (right)
  box(root, lambert({ color: night ? "#2a2348" : "#d9c7e2" }), W, 0.3, Z1 - Z0, 0, H + 0.15, (Z0 + Z1) / 2); // ceiling
  // cornice and wainscot
  for (const s of [-1, 1]) {
    box(root, gold, 0.4, 0.45, Z1 - Z0, s * (W / 2 - 0.2), H - 0.3, (Z0 + Z1) / 2);
    box(root, lambert({ color: night ? "#5b5288" : "#c8b2d8" }), 0.12, 1.1, Z1 - Z0, s * (W / 2 - 0.06), 0.55, (Z0 + Z1) / 2);
  }
  box(root, gold, W, 0.45, 0.4, 0, H - 0.3, Z0 + 0.2);
  // pilasters, windows (left), mirrors (right)
  const skyT = night ? skyGrad("#0b1336", "#1d2a63", "#3b3f7a", 160) : skyGrad("#7fa7d6", "#bcd2e6", "#f6e3bd");
  const glassMat = basic({ map: skyT });
  const mirror = lambert({ color: night ? "#4a5a9a" : "#b9d4ea" });
  for (let z = Z0 + 2; z < Z1; z += 4) {
    for (const s of [-1, 1]) box(root, gold, 0.5, H - 0.8, 0.5, s * (W / 2 - 0.25), (H - 0.8) / 2, z - 2);
    const win = new THREE.Mesh(arch(2.0, 5.0), glassMat); win.position.set(X0 + 0.02, 1.0, z); win.rotation.y = Math.PI / 2; win.layers.set(NOINK); root.add(win);
    const frame = new THREE.Mesh(arch(2.3, 5.2), gold); frame.position.set(X0 + 0.01, 0.9, z); frame.rotation.y = Math.PI / 2; root.add(frame);
    box(root, gold, 0.06, 5.0, 0.07, X0 + 0.05, 3.5, z);
    box(root, gold, 0.06, 0.07, 2.0, X0 + 0.05, 3.2, z);
    const mir = new THREE.Mesh(arch(1.8, 4.6), mirror); mir.position.set(-X0 - 0.02, 1.2, z); mir.rotation.y = -Math.PI / 2; root.add(mir);
    if (night) glows.push(glowSprite(root, [120, 140, 255], 3.2, X0 + 0.4, 3.4, z));
    else glows.push(glowSprite(root, [255, 236, 190], 3.0, X0 + 0.5, 3.0, z));
  }
  // throne dais with drapes
  box(root, lac, 5, 0.25, 3, 0, 0.125, Z0 + 1.6);
  box(root, lac, 4, 0.25, 2.2, 0, 0.375, Z0 + 1.3);
  const drape = lambert({ color: "#9c2a3a" });
  for (const s of [-1, 1]) box(root, drape, 1.4, 6.2, 0.2, s * 2.4, 3.1, Z0 + 0.35);
  box(root, drape, 6.2, 1.0, 0.25, 0, 6.6, Z0 + 0.4);
  box(root, gold, 1.2, 0.6, 1.0, 0, 0.8, Z0 + 1.2);
  box(root, lambert({ color: "#b5283a" }), 1.0, 1.8, 0.2, 0, 1.6, Z0 + 0.8);
  // entrance doors
  for (const s of [-1, 1]) box(root, lambert({ color: night ? "#4d3a5a" : "#e7d6b0" }), 1.2, 3.6, 0.15, s * 0.62, 1.8, Z1 - 0.05);
  // chandeliers
  for (const z of [-12, -5, 2]) {
    cyl(root, gold, 0.03, 1.6, 0, H - 0.8, z, 6);
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.9, 0.06, 8, 32), gold); ring.rotation.x = Math.PI / 2; ring.position.set(0, H - 1.7, z); root.add(ring);
    for (let k = 0; k < 8; k++) {
      const a = (k / 8) * Math.PI * 2;
      cyl(root, lambert({ color: "#f4eee1" }), 0.04, 0.25, Math.cos(a) * 0.9, H - 1.55, z + Math.sin(a) * 0.9, 6);
      const fl = new THREE.Mesh(new THREE.SphereGeometry(0.05, 8, 6), basic({ color: "#ffd27a" })); fl.layers.set(NOINK);
      fl.position.set(Math.cos(a) * 0.9, H - 1.37, z + Math.sin(a) * 0.9); root.add(fl);
    }
    glows.push(glowSprite(root, [255, 210, 130], night ? 5.0 : 2.4, 0, H - 1.5, z));
  }
  const key = night ? makeKey(root, [-14, 12, -2], [0, 0, -6], 14) : makeKey(root, [-14, 13, 4], [0, 0, -6], 14);
  return { root, key, glows, extra: {} };
}

function runner() {
  const c = document.createElement("canvas"); c.width = 256; c.height = 256;
  const g = c.getContext("2d")!;
  g.fillStyle = "#8c2230"; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#d6a640"; g.fillRect(0, 0, 18, 256); g.fillRect(238, 0, 18, 256);
  g.fillStyle = "#2b3d6b"; g.fillRect(26, 0, 8, 256); g.fillRect(222, 0, 8, 256);
  g.strokeStyle = "rgba(214, 166, 64, 0.6)"; g.lineWidth = 6;
  g.beginPath(); g.moveTo(128, 30); g.lineTo(180, 128); g.lineTo(128, 226); g.lineTo(76, 128); g.closePath(); g.stroke();
  return c;
}

// ------------------------------------------------------------------------------------------------ Paris salon, 1783
export function salonSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: marbleChecker([3, 3]) }), 10, 10, 0, 0, -2, -Math.PI / 2);
  const wall = lambert({ map: panelWall([3, 1], "#7fb7a2", "#d9c48a") });
  const cream = lambert({ color: "#efe3c8" });
  const gold = lambert({ map: brass() });
  box(root, wall, 10, 5.2, 0.3, 0, 2.6, -7);
  box(root, wall, 0.3, 5.2, 10, -5, 2.6, -2);
  box(root, wall, 0.3, 5.2, 10, 5, 2.6, -2);
  box(root, lambert({ color: "#e9dcc0" }), 10, 0.3, 10, 0, 5.35, -2);
  box(root, cream, 10, 0.3, 0.35, 0, 5.0, -6.85);
  // fireplace with a mirror, a fire glow
  box(root, cream, 2.6, 1.4, 0.6, 1.6, 0.7, -6.6);
  box(root, lambert({ color: "#1e1a24" }), 1.4, 0.9, 0.2, 1.6, 0.45, -6.35, false);
  box(root, cream, 3.0, 0.15, 0.8, 1.6, 1.45, -6.6);
  box(root, gold, 1.8, 2.0, 0.08, 1.6, 2.6, -6.84);
  box(root, lambert({ color: "#bfe0ec" }), 1.5, 1.7, 0.05, 1.6, 2.6, -6.79, false);
  glows.push(glowSprite(root, [255, 150, 60], 1.8, 1.6, 0.5, -6.1));
  // tall window with Paris roofs behind
  const win = new THREE.Mesh(arch(1.8, 3.8), basic({ map: parisView() })); win.position.set(-4.84, 0.6, -3.5); win.rotation.y = Math.PI / 2; win.layers.set(NOINK); root.add(win);
  const fr = new THREE.Mesh(arch(2.1, 4.0), cream); fr.position.set(-4.85, 0.5, -3.5); fr.rotation.y = Math.PI / 2; root.add(fr);
  glows.push(glowSprite(root, [255, 236, 200], 3.0, -4.4, 2.4, -3.5));
  // bookcase and sofa
  const wood = lambert({ color: "#6e4527" });
  box(root, wood, 0.5, 3.2, 2.2, 4.7, 1.6, -4.6);
  const cols = ["#9e2f2a", "#2c4f7a", "#3d7a4a", "#c99a3a", "#5a2f7a", "#d8cbb0"];
  for (let r = 0; r < 4; r++) for (let k = 0; k < 7; k++) box(root, lambert({ color: cols[(r * 3 + k) % 6] }), 0.3, 0.55, 0.24, 4.45, 0.45 + r * 0.75, -5.5 + k * 0.28, false);
  box(root, lambert({ color: "#b8456a" }), 2.2, 0.5, 0.9, -2.6, 0.45, -6.1);
  box(root, lambert({ color: "#a03a5c" }), 2.2, 0.8, 0.25, -2.6, 0.9, -6.5);
  const key = makeKey(root, [-10, 9, 3], [0, 0, -3], 9);
  return { root, key, glows, extra: {} };
}
function parisView() {
  const c = document.createElement("canvas"); c.width = 256; c.height = 512;
  const g = c.getContext("2d")!;
  const grd = g.createLinearGradient(0, 0, 0, 512); grd.addColorStop(0, "#8fb6dc"); grd.addColorStop(1, "#f3dcb4");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 512);
  g.fillStyle = "#5d6f96";
  g.beginPath(); g.moveTo(0, 330); for (let x = 0; x <= 256; x += 32) g.lineTo(x, 300 + ((x / 32) % 2) * 26); g.lineTo(256, 512); g.lineTo(0, 512); g.fill();
  g.fillStyle = "#e9e0cc"; g.fillRect(30, 260, 10, 50); g.fillRect(180, 250, 10, 60);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}

// ------------------------------------------------------------------------------------------------ touring map on a table
export function mapTableSet(mapCanvas: HTMLCanvasElement): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  box(root, lambert({ map: darkBoards([2, 2]) }), 4.2, 0.12, 3.0, 0, 0.74, 0);
  for (const [x, z] of [[-1.9, -1.3], [1.9, -1.3], [-1.9, 1.3], [1.9, 1.3]]) box(root, lambert({ color: "#4b2e1a" }), 0.14, 0.74, 0.14, x, 0.37, z);
  plane(root, lambert({ color: "#3a2a3e" }), 30, 30, 0, 0, 0, -Math.PI / 2);
  const mt = new THREE.CanvasTexture(mapCanvas); mt.colorSpace = THREE.SRGBColorSpace; mt.anisotropy = 8;
  const map = plane(root, lambert({ map: mt }), 3.4, 2.4, 0, 0.805, 0, -Math.PI / 2);
  map.receiveShadow = true;
  box(root, lambert({ map: stoneWall([4, 2], 30, 40) }), 30, 8, 0.3, 0, 4, -6);
  // a brass compass and a candle on the table
  cyl(root, lambert({ map: brass() }), 0.16, 0.04, 1.7, 0.82, 1.1);
  cyl(root, lambert({ color: "#f4eee1" }), 0.05, 0.3, -1.75, 0.95, -1.05, 10);
  glows.push(glowSprite(root, [255, 190, 110], 1.6, -1.75, 1.18, -1.05));
  const key = makeKey(root, [-6, 9, 5], [0, 0.8, 0], 5);
  return { root, key, glows, extra: { map } };
}

// ------------------------------------------------------------------------------------------------ Philadelphia museum, 1854
export function museumSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: paving([8, 8], 230, 42, 9) }), 60, 60, 0, 0, -6, -Math.PI / 2);
  const stone = lambert({ map: stoneWall([3, 2], 222, 52) });
  box(root, stone, 18, 9, 3, 0, 4.5, -10);
  box(root, lambert({ color: "#3c4160" }), 18.6, 0.8, 3.4, 0, 9.4, -10);
  const ped = new THREE.Shape(); ped.moveTo(-6, 0); ped.lineTo(6, 0); ped.lineTo(0, 2.4); ped.lineTo(-6, 0);
  const pm = new THREE.Mesh(new THREE.ExtrudeGeometry(ped, { depth: 0.6, bevelEnabled: false }), lambert({ color: "#9aa0bd" }));
  pm.position.set(0, 9.8, -8.7); pm.castShadow = true; root.add(pm);
  const sign = plane(root, lambert({ map: signTex("MUSEUM", 1024, 192, "#2f3352", "#f1e3c0") }), 6, 1.1, 0, 8.4, -8.42);
  sign.castShadow = false;
  const col = lambert({ color: "#c9cbe0" });
  for (let i = 0; i < 6; i++) cyl(root, col, 0.36, 7.2, -5 + i * 2, 3.6, -8.2);
  const win: THREE.Mesh[] = [];
  for (let k = 0; k < 5; k++) for (let row = 0; row < 2; row++) {
    const m = box(root, basic({ color: "#232846" }), 1.1, 1.9, 0.1, -6 + k * 3, 2.2 + row * 3.4, -8.45, false);
    win.push(m);
  }
  const iron = lambert({ color: "#1d1d2a" });
  for (const x of [-7, 7]) { cyl(root, iron, 0.07, 4, x, 2, -2, 8); glows.push(glowSprite(root, [255, 200, 120], 1.6, x, 4.1, -2)); }
  const sky = skyCard(root, skyGrad("#070b24", "#18204e", "#3a2a4e", 220), 160, 70, 0, 24, -30);
  const key = makeKey(root, [6, 14, 10], [0, 0, -8], 16);
  return { root, key, glows, sky, extra: Object.fromEntries(win.map((m, i) => [`win${i}`, m])) };
}

/** the burning gallery inside the museum: dark stone room, the Turk on its cabinet among the flames */
export function galleryInteriorSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: darkBoards([3, 3]) }), 20, 20, 0, 0, -3, -Math.PI / 2);
  const stone = lambert({ map: stoneWall([3, 2], 240, 30) });
  box(root, stone, 14, 7, 0.3, 0, 3.5, -8);
  box(root, stone, 0.3, 7, 14, -6, 3.5, -2);
  box(root, stone, 0.3, 7, 14, 6, 3.5, -2);
  for (const x of [-3.5, 3.5]) cyl(root, lambert({ color: "#5b5f7c" }), 0.32, 7, x, 3.5, -6.5);
  // display cases and frames on the walls (the Chinese Museum's collection)
  for (const x of [-4.5, 4.5]) box(root, lambert({ color: "#4a3326" }), 1.2, 1.0, 0.7, x, 0.5, -6.8);
  for (const x of [-2, 2]) box(root, lambert({ color: "#b8873c" }), 1.4, 1.0, 0.06, x, 3.6, -7.82);
  const key = makeKey(root, [5, 8, 6], [0, 0, -3], 9);
  return { root, key, glows, extra: {} };
}

// ------------------------------------------------------------------------------------------------ night workshop
export function workshopSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: darkBoards([3, 3]) }), 16, 16, 0, 0, -2, -Math.PI / 2);
  const stone = lambert({ map: stoneWall([3, 2], 228, 40) });
  box(root, stone, 12, 6, 0.3, 0, 3, -6);
  box(root, stone, 0.3, 6, 12, -6, 3, -1);
  box(root, stone, 0.3, 6, 12, 6, 3, -1);
  // tall window with the moon
  const win = new THREE.Mesh(arch(1.6, 3.2), basic({ map: skyGrad("#08112e", "#16245a", "#2a3a7a", 120) }));
  win.position.set(-2.6, 1.4, -5.84); win.layers.set(NOINK); root.add(win);
  const moon = new THREE.Mesh(new THREE.CircleGeometry(0.22, 24), basic({ color: "#f4f1e4" })); moon.position.set(-2.4, 3.6, -5.82); moon.layers.set(NOINK); root.add(moon);
  glows.push(glowSprite(root, [140, 160, 255], 3.4, -2.6, 3.0, -5.6));
  // workbench, tools, shelves (the automaton maker's room)
  const wood = lambert({ color: "#5b3b25" });
  box(root, wood, 2.8, 0.12, 1.0, 3.6, 0.95, -5.1);
  for (const x of [2.4, 4.8]) box(root, wood, 0.12, 0.95, 0.9, x, 0.475, -5.1);
  box(root, wood, 2.6, 0.08, 0.4, 3.6, 2.4, -5.7);
  box(root, wood, 2.6, 0.08, 0.4, 3.6, 3.1, -5.7);
  const b = lambert({ map: brass() });
  for (let k = 0; k < 5; k++) cyl(root, b, 0.12 + (k % 2) * 0.06, 0.03, 2.7 + k * 0.45, 2.5, -5.6, 16);
  const key = makeKey(root, [-8, 9, -2], [0, 0, -2], 7);
  return { root, key, glows, extra: {} };
}
