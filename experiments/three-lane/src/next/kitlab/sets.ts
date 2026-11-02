// KitLab's own places and props (our own code, lab content only): the keeper's lamp room (clock, window, a framed
// photo beside the clock, a bell rope), the inside of the clock (gear room), the night sea seen from the lighthouse,
// a ship's deck in the harbour by day, and props (brass key, gears, the stone weight). Built on the kit's set helpers.
import * as THREE from "three";
import { NOINK } from "../../ink";
import { rng, plaster } from "../../paint";
import { lambert, basic, box, cyl, plane, glowSprite, skyDome, makeKey, type SetBuild } from "../../kit/sets";
import { brass, darkBoards, tex } from "../../kit/paint2";
import { grainPlanks, stoneCourses, richWater, dress, clouds, crate, barrel, ropeCoil, net, sack } from "../../kit/dressing";

const INK = "#1b1240";
const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const ctex = (c: HTMLCanvasElement) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; };

// ------------------------------------------------------------------------------------------------ props
/** a brass gear: disc + teeth + hub, lying in the xy plane (axis along z) */
export function gear(r: number, teeth: number, th = 0.08, color?: string, missing = -1) {
  const g = new THREE.Group();
  const m = color ? lambert({ color }) : lambert({ map: brass() });
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(r, r, th, 40), m); disc.rotation.x = Math.PI / 2; disc.castShadow = true; disc.receiveShadow = true; g.add(disc);
  for (let i = 0; i < teeth; i++) {
    if (i === missing) continue;
    const a = (i / teeth) * Math.PI * 2;
    const t = new THREE.Mesh(new THREE.BoxGeometry(r * 0.16, r * 0.2, th), m);
    t.position.set(Math.cos(a) * (r + r * 0.08), Math.sin(a) * (r + r * 0.08), 0); t.rotation.z = a - Math.PI / 2; t.castShadow = true; g.add(t);
  }
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.2, r * 0.2, th * 1.6, 20), lambert({ color: "#5a4030" })); hub.rotation.x = Math.PI / 2; g.add(hub);
  for (let k = 0; k < 4; k++) { const s = new THREE.Mesh(new THREE.BoxGeometry(r * 1.4, r * 0.1, th * 1.05), lambert({ color: "#8a6a2a" })); s.rotation.z = (k * Math.PI) / 4; g.add(s); }
  return g;
}
/** the brass winding key (bow ring, shaft, bit), lying along x, bow at the origin */
export function brassKey(s = 1) {
  const g = new THREE.Group(), m = lambert({ map: brass() });
  const bow = new THREE.Mesh(new THREE.TorusGeometry(0.05 * s, 0.014 * s, 10, 28), m); bow.rotation.x = Math.PI / 2; bow.castShadow = true; g.add(bow);
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.011 * s, 0.011 * s, 0.2 * s, 12), m); shaft.rotation.z = Math.PI / 2; shaft.position.x = 0.15 * s; shaft.castShadow = true; g.add(shaft);
  for (const [x, h] of [[0.22, 0.03], [0.24, 0.045], [0.235, 0.02]] as const) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.012 * s, h * s, 0.012 * s), m); b.position.set(x * s, -h * s * 0.5, 0); g.add(b); }
  return g;
}
/** the stone weight on its rope (pivot at the rope top) */
export function weight(len: number) {
  const g = new THREE.Group();
  const rope = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, len, 6), lambert({ color: "#7a5a3a" })); rope.position.y = -len / 2; g.add(rope);
  const st = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.32, 0.5, 8), lambert({ color: "#b8b4c4" })); st.position.y = -len - 0.25; st.castShadow = true; g.add(st);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.018, 8, 16), lambert({ color: "#4a4050" })); ring.position.y = -len + 0.02; g.add(ring);
  return { g, stone: st };
}
/** a clock dial texture (numerals, ring); hands are separate meshes so they can turn */
function dialTex() {
  const [c, g] = canvas(512, 512);
  g.fillStyle = "#f3ead2"; g.beginPath(); g.arc(256, 256, 250, 0, Math.PI * 2); g.fill();
  g.strokeStyle = INK; g.lineWidth = 14; g.stroke();
  g.lineWidth = 6; g.beginPath(); g.arc(256, 256, 206, 0, Math.PI * 2); g.stroke();
  g.fillStyle = INK; g.font = '800 54px "Montserrat", Arial'; g.textAlign = "center"; g.textBaseline = "middle";
  const R = ["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"];
  R.forEach((s, i) => { const a = (i / 12) * Math.PI * 2 - Math.PI / 2; g.fillText(s, 256 + Math.cos(a) * 168, 256 + Math.sin(a) * 168); });
  return ctex(c);
}
/** a painted picture for the wall frame before the photo arrives (a small seascape) */
function seascape() {
  const [c, g] = canvas(256, 456);
  const grd = g.createLinearGradient(0, 0, 0, 456); grd.addColorStop(0, "#9fb8de"); grd.addColorStop(0.55, "#f0d6b0"); grd.addColorStop(0.56, "#4f7fa6"); grd.addColorStop(1, "#2c4f78");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 456);
  g.fillStyle = "#f3ead2"; g.fillRect(150, 150, 22, 104); g.fillStyle = "#c8402e"; g.fillRect(150, 180, 22, 16); g.fillRect(150, 214, 22, 16);
  return ctex(c);
}

// ------------------------------------------------------------------------------------------------ the lamp room
// floor x -4..4, z -6..2, back wall z = -6 (clock right, photo left of it), window in the left wall (x = -4)
export const ROOM = { clock: [1.3, 2.3, -5.84] as [number, number, number], clockR: 0.85, photo: [-0.55, 2.05, -5.85] as [number, number, number], photoW: 0.45, photoH: 0.8,
  window: [-3.97, 2.05, -2.6] as [number, number, number], winW: 1.3, winH: 1.9, rope: [2.9, 0, -4.6] as [number, number, number] };
/** the four corners (TL, TR, BR, BL) of the wall photo's picture area, in world space */
export const photoQuad = (): [number, number, number][] => {
  const [x, y, z] = ROOM.photo, w = ROOM.photoW / 2, h = ROOM.photoH / 2;
  return [[x - w, y + h, z + 0.035], [x + w, y + h, z + 0.035], [x + w, y - h, z + 0.035], [x - w, y - h, z + 0.035]];
};
/** the window opening (seen from inside the room, looking -x): TL, TR, BR, BL */
export const windowQuad = (): [number, number, number][] => {
  const [x, y, z] = ROOM.window, w = ROOM.winW / 2, h = ROOM.winH / 2;
  return [[x + 0.02, y + h, z + w], [x + 0.02, y + h, z - w], [x + 0.02, y - h, z - w], [x + 0.02, y - h, z + w]];
};
export function roomSet(o: { night?: boolean } = {}): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: grainPlanks([3, 3], { hue: 30, light: o.night ? 36 : 46, boards: 6, seed: 4 }) }), 8, 8, 0, 0, -2, -Math.PI / 2);
  const wallM = lambert({ map: plaster([2, 1]), color: o.night ? "#c4c0e2" : "#f4e8da" });
  box(root, wallM, 8, 4.2, 0.3, 0, 2.1, -6.15);
  box(root, wallM, 8, 4.2, 0.3, 0, 2.1, 2.15);
  box(root, wallM, 0.3, 4.2, 8, 4.15, 2.1, -2);
  // left wall with the window opening (four boxes round the hole)
  const [wx, wy, wz] = ROOM.window, ww = ROOM.winW, wh = ROOM.winH;
  const zA = -6, zB = wz - ww / 2, zC = wz + ww / 2, zD = 2;
  box(root, wallM, 0.3, 4.2, zB - zA, -4.15, 2.1, (zA + zB) / 2);
  box(root, wallM, 0.3, 4.2, zD - zC, -4.15, 2.1, (zC + zD) / 2);
  box(root, wallM, 0.3, wy - wh / 2, ww, -4.15, (wy - wh / 2) / 2, wz);
  box(root, wallM, 0.3, 4.2 - (wy + wh / 2), ww, -4.15, (4.2 + wy + wh / 2) / 2, wz);
  const wood = lambert({ color: o.night ? "#4d3a5a" : "#7a4a2a" });
  for (const dz of [-ww / 2, ww / 2]) box(root, wood, 0.36, wh + 0.2, 0.1, wx, wy, wz + dz);
  for (const dy of [-wh / 2, wh / 2]) box(root, wood, 0.36, 0.1, ww + 0.2, wx, wy + dy, wz);
  box(root, wood, 0.1, wh, 0.05, wx, wy, wz); box(root, wood, 0.1, 0.05, ww, wx, wy, wz);
  // outside the window: a sky + sea card (the push-through shows the real sea shot through the opening)
  const [sc, sg] = canvas(256, 512);
  const grd = sg.createLinearGradient(0, 0, 0, 512);
  if (o.night) { grd.addColorStop(0, "#0b1336"); grd.addColorStop(0.55, "#2a2f6a"); grd.addColorStop(0.56, "#18305a"); grd.addColorStop(1, "#0e1d3c"); }
  else { grd.addColorStop(0, "#7fa7d6"); grd.addColorStop(0.55, "#f2dcb4"); grd.addColorStop(0.56, "#4f8fb0"); grd.addColorStop(1, "#2f6a8e"); }
  sg.fillStyle = grd; sg.fillRect(0, 0, 256, 512);
  const out = plane(root, basic({ map: ctex(sc) }), 30, 24, -14, 3, -2.6, 0, Math.PI / 2); out.layers.set(NOINK);
  glows.push(glowSprite(root, o.night ? [120, 140, 255] : [255, 236, 200], 2.6, wx + 0.5, wy, wz));
  box(root, lambert({ color: o.night ? "#2a2348" : "#e6d6c6" }), 8, 0.3, 8, 0, 4.35, -2);
  box(root, lambert({ map: grainPlanks([4, 1], { hue: 24, light: o.night ? 30 : 38, boards: 2, seed: 8, vertical: true }) }), 8, 0.9, 0.08, 0, 0.45, -5.98);   // wainscot
  box(root, lambert({ map: grainPlanks([4, 1], { hue: 24, light: o.night ? 30 : 38, boards: 2, seed: 9, vertical: true }) }), 0.08, 0.9, 8, 4.0, 0.45, -2);
  // shelves on the right wall: jars, books, a coil of rope; the floor dressed with the keeper's stores
  for (const y of [1.6, 2.3]) {
    box(root, lambert({ color: "#6b4426" }), 0.35, 0.06, 2.2, 3.82, y, -1.6);
    const r = rng(Math.round(y * 10));
    for (let k = 0; k < 9; k++) {
      const kind = r();
      if (kind < 0.5) box(root, lambert({ color: ["#9e2f2a", "#2c4f7a", "#3d7a4a", "#c99a3a", "#5a2f7a"][k % 5] }), 0.22, 0.28 + r() * 0.1, 0.08, 3.82, y + 0.17, -2.6 + k * 0.22, false);
      else cyl(root, lambert({ color: kind < 0.75 ? "#8fb8c8" : "#d8c49a" }), 0.07, 0.2, 3.82, y + 0.13, -2.6 + k * 0.22, 10);
    }
  }
  const coil = ropeCoil(0.22); coil.position.set(3.82, 2.36, -0.8); root.add(coil);
  const keep = ([[0.5, -5.0], [0.15, -4.4], [-3.3, -0.95], [2.45, -4.35], [-1.35, -4.4], [-1.9, -5.2], [2.9, -4.6]] as [number, number][]).map(([x, z]) => [x - 0.75, 0, z - 0.75, x + 0.75, 3, z + 0.75] as [number, number, number, number, number, number]);
  keep.push([-1.2, 0, -6, 2.4, 3, -5.0], [-4, 0, -3.6, -2.6, 3, -1.4]);
  dress(root, { area: [-3.6, -5.7, 3.6, 0.8], n: 9, kit: ["crate", "barrel", "sack", "bucket", "ropeCoil"], keep, seed: o.night ? 12 : 12, scale: 0.9 });
  // the clock: case, dial, hands
  const [cx, cy, cz] = ROOM.clock, R = ROOM.clockR;
  const caseM = lambert({ color: "#6b3f22" });
  const cs = new THREE.Mesh(new THREE.CylinderGeometry(R + 0.12, R + 0.12, 0.22, 40), caseM); cs.rotation.x = Math.PI / 2; cs.position.set(cx, cy, cz + 0.05); cs.castShadow = true; root.add(cs);
  const dial = new THREE.Mesh(new THREE.CircleGeometry(R, 48), lambert({ map: dialTex() })); dial.position.set(cx, cy, cz + 0.17); root.add(dial);
  const hand = (len: number, w: number) => { const h = new THREE.Group(); const m = new THREE.Mesh(new THREE.BoxGeometry(w, len, 0.02), lambert({ color: INK })); m.position.y = len / 2 - 0.04; h.add(m); h.position.set(cx, cy, cz + 0.2); root.add(h); return h; };
  const hour = hand(R * 0.55, 0.06), minute = hand(R * 0.82, 0.04);
  const keyhole = new THREE.Mesh(new THREE.CircleGeometry(0.035, 16), basic({ color: "#2a1a10" })); keyhole.position.set(cx + 0.3, cy - 0.32, cz + 0.18); root.add(keyhole);
  // the framed picture beside the clock (9:16 picture area) and its glass
  const [px, py, pz] = ROOM.photo;
  box(root, lambert({ color: "#b8873c" }), ROOM.photoW + 0.14, ROOM.photoH + 0.14, 0.05, px, py, pz);
  const pic = plane(root, lambert({ map: seascape() }), ROOM.photoW, ROOM.photoH, px, py, pz + 0.03);
  // bell rope from the ceiling, a table with a lantern, a stool
  cyl(root, lambert({ color: "#b99060" }), 0.025, 3.0, ROOM.rope[0], 2.7, ROOM.rope[2], 6);
  const tassel = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.2, 8), lambert({ color: "#c8402e" })); tassel.position.set(ROOM.rope[0], 1.15, ROOM.rope[2]); root.add(tassel);
  box(root, lambert({ map: darkBoards([1, 1]) }), 1.6, 0.08, 0.8, -1.9, 0.86, -5.2);
  for (const [x, z] of [[-2.6, -5.5], [-1.2, -5.5], [-2.6, -4.9], [-1.2, -4.9]]) box(root, lambert({ color: "#4b2e1a" }), 0.07, 0.86, 0.07, x, 0.43, z);
  cyl(root, lambert({ map: brass() }), 0.12, 0.32, -2.3, 1.06, -5.25, 12);
  glows.push(glowSprite(root, [255, 196, 120], o.night ? 2.2 : 1.0, -2.3, 1.2, -5.15));
  glows.push(glowSprite(root, [255, 210, 150], 1.6, cx, cy, cz + 0.4));
  const key = o.night ? makeKey(root, [-9, 7, 3], [0, 1, -3], 8) : makeKey(root, [-10, 8, 2], [0, 1, -3], 8);
  return { root, key, glows, extra: { hour, minute, pic, dial } };
}
/** turn the clock hands (h = clock hours, eased steps allowed by the caller) */
export const clockHands = (s: SetBuild, h: number) => {
  s.extra.hour.rotation.z = -((h % 12) / 12) * Math.PI * 2;
  s.extra.minute.rotation.z = -((h % 1) * Math.PI * 2);
};

// ------------------------------------------------------------------------------------------------ inside the clock
export function gearRoomSet(): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: grainPlanks([4, 4], { hue: 24, light: 30, seed: 6 }) }), 12, 12, 0, 0, -2, -Math.PI / 2);
  box(root, lambert({ map: stoneCourses([3, 2], { hue: 28, light: 46, seed: 3 }) }), 12, 6, 0.3, 0, 3, -4.5);
  box(root, lambert({ map: stoneCourses([3, 2], { hue: 28, light: 46, seed: 5 }) }), 0.3, 6, 12, -4, 3, -1);
  // the clockwork's own clutter: chains hanging, a spare-parts crate, oil cans
  for (const [x, z] of [[-2.8, -3.8], [2.9, -3.9], [-3.4, -1.6]] as [number, number][]) cyl(root, lambert({ color: "#4a4050" }), 0.025, 5.6, x, 3.2, z, 6);
  const cr = crate(0.6); cr.position.set(-2.9, 0, -2.6); root.add(cr);
  const cr2 = crate(0.45); cr2.position.set(-2.85, 0.6, -2.55); cr2.rotation.y = 0.4; root.add(cr2);
  for (let k = 0; k < 3; k++) cyl(root, lambert({ color: "#5a6a3a" }), 0.08, 0.22, 2.4 + k * 0.22, 0.31, -2.4, 10);
  const big = gear(1.4, 28, 0.2, undefined, 7); big.position.set(1.2, 2.2, -3.6); root.add(big);
  const mid = gear(0.8, 16, 0.18); mid.position.set(-0.95, 1.7, -3.4); root.add(mid);
  const small = gear(0.45, 10, 0.16); small.position.set(-0.6, 3.25, -3.3); root.add(small);
  // the broken tooth (lies on the floor until it is hammered back) and a beam to stand on
  const tooth = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.28, 0.2), lambert({ map: brass() })); tooth.castShadow = true; root.add(tooth);
  box(root, lambert({ color: "#5b3b25" }), 6, 0.2, 0.9, 0, 0.1, -2.2);
  glows.push(glowSprite(root, [255, 196, 120], 2.4, -2.6, 2.6, -3.0));
  const key = makeKey(root, [-6, 8, 4], [0, 1.5, -3], 6);
  return { root, key, glows, extra: { big, mid, small, tooth } };
}

// ------------------------------------------------------------------------------------------------ the night sea
export function seaSet(): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  const [c, g] = canvas(512, 512); const r = rng(5);
  g.fillStyle = "#1f3f66"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 30; i++) { const x = r() * 512, y = r() * 512, w = 40 + r() * 90; g.strokeStyle = "rgba(160, 200, 240, 0.4)"; g.lineWidth = 3 + r() * 3; g.lineCap = "round"; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 8, x + w, y); g.stroke(); }
  void c; void g;
  const water = plane(root, lambert({ map: richWater([60, 60], { deep: true, seed: 5 }) }), 600, 600, 0, 0, -100, -Math.PI / 2);
  clouds(root, { n: 9, x: [-90, 90], y: [30, 70], z: [-240, -160], size: 60, tint: "#9aa4d8" });
  skyDome(root, "#070b24", "#1d2a63", "#3b3f7a", 800, 220);
  const moon = new THREE.Mesh(new THREE.CircleGeometry(4, 32), basic({ color: "#f4f1e4" })); moon.position.set(-30, 40, -200); moon.layers.set(NOINK); root.add(moon);
  glows.push(glowSprite(root, [150, 170, 255], 40, -30, 40, -199));
  // rocks in the foreground and mid-ground
  const rock = lambert({ color: "#4a4a62" });
  for (const [x, z, s] of [[-6, -18, 2.4], [-2, -22, 1.6], [4, -20, 2.0], [8, -26, 1.2], [1, -40, 3.0]]) { const m = new THREE.Mesh(new THREE.DodecahedronGeometry(s), rock); m.position.set(x, s * 0.3, z); m.castShadow = true; root.add(m); }
  // the ship: hull, deck house, mast, a sail, a lantern
  const ship = new THREE.Group();
  box(ship, lambert({ color: "#6b3f22" }), 6, 1.4, 1.8, 0, 0.5, 0); box(ship, lambert({ color: "#8a5a32" }), 1.4, 0.8, 1.2, -1.5, 1.6, 0);
  cyl(ship, lambert({ color: "#5b3b25" }), 0.08, 5, 0.6, 3.6, 0, 8);
  const sail = box(ship, lambert({ color: "#efe3c8" }), 0.06, 3.0, 2.6, 0.8, 3.6, 0); sail.rotation.y = 0.15;
  glows.push(glowSprite(ship, [255, 200, 120], 2.2, 2.6, 1.6, 0));
  ship.position.set(10, 0, -70); root.add(ship);
  const key = makeKey(root, [-30, 40, -20], [0, 0, -40], 60);
  return { root, key, glows, extra: { ship, water }, fogScale: 4 };
}

// ------------------------------------------------------------------------------------------------ the ship's deck by day
export function deckSet(): SetBuild {
  const root = new THREE.Group(), glows: THREE.Object3D[] = [];
  const [c, g] = canvas(512, 512); const r = rng(9);
  g.fillStyle = "#3f8fa6"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 26; i++) { const x = r() * 512, y = r() * 512, w = 40 + r() * 90; g.strokeStyle = "rgba(220, 245, 250, 0.55)"; g.lineWidth = 4; g.lineCap = "round"; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 8, x + w, y); g.stroke(); }
  void c; void g;
  plane(root, lambert({ map: richWater([40, 40], { seed: 9 }) }), 400, 400, 0, -1.2, -50, -Math.PI / 2);
  clouds(root, { n: 8, x: [-60, 60], y: [18, 40], z: [-120, -80], size: 26 });
  const planks = lambert({ map: grainPlanks([2, 6], { hue: 30, light: 50, seed: 2 }) });
  box(root, planks, 4.4, 0.2, 9, 0, -0.1, -2);
  for (const s of [-1, 1]) box(root, lambert({ color: "#6b3f22" }), 0.25, 0.9, 9, s * 2.2, 0.35, -2);
  cyl(root, lambert({ color: "#5b3b25" }), 0.12, 9, 0, 4.5, -4.5, 10);
  box(root, lambert({ color: "#efe3c8" }), 3.6, 3.4, 0.05, 0, 5.2, -4.35);
  // cargo, rope and nets round the crew (they stand in x -1.4..1.4, z -2.4..-1.0)
  const keepCrew: [number, number, number, number, number, number][] = [[-1.5, -1, -2.6, 1.5, 3, 3]];
  dress(root, { area: [-2.0, -6.2, 2.0, -2.7], n: 10, kit: ["crate", "barrel", "ropeCoil", "sack"], keep: keepCrew, seed: 21 });
  dress(root, { area: [-2.0, -2.6, -1.5, 1.0], n: 3, kit: ["barrel", "ropeCoil", "bucket"], keep: [], seed: 22 });
  dress(root, { area: [1.5, -2.6, 2.0, 1.0], n: 3, kit: ["crate", "sack", "bucket"], keep: [], seed: 23 });
  const nt = net(1.8, 1.4); nt.position.set(-2.12, 0.2, -4.0); nt.rotation.y = Math.PI / 2; root.add(nt);
  const b1 = barrel(0.8); b1.position.set(1.7, 0, -3.2); root.add(b1); const s1 = sack(0.5); s1.position.set(1.2, 0, -3.0); root.add(s1);
  // the harbour town behind
  const town = lambert({ color: "#d9b48a" }), roofM = lambert({ color: "#b24a32" });
  for (let i = 0; i < 9; i++) { const x = -24 + i * 6, h = 4 + r() * 5; box(root, town, 5, h, 4, x, h / 2 - 1.2, -40); box(root, roofM, 5.2, 1, 4.2, x, h - 0.7, -40); }
  skyDome(root, "#5f93d0", "#bcd2e6", "#f0dcb4", 600);
  const key = makeKey(root, [8, 12, 10], [0, 0, -2], 8);
  return { root, key, glows, extra: {} };
}

// ------------------------------------------------------------------------------------------------ x-ray drawings
/** the casing as seen from outside (wooden clock casing) and the same casing scanned (cyan line art, one gear with a
 * snapped tooth circled in red) */
export function xrayCanvases() {
  const draw = (inside: boolean) => {
    const [c, g] = canvas(640, 880);
    g.fillStyle = inside ? "#08202c" : "#6b3f22"; g.fillRect(0, 0, 640, 880);
    if (!inside) {
      g.fillStyle = "#7d4c2a"; for (let y = 0; y < 880; y += 80) g.fillRect(0, y + 4, 640, 72);
      g.strokeStyle = INK; g.lineWidth = 10; g.strokeRect(40, 40, 560, 800);
      g.fillStyle = "#f3ead2"; g.beginPath(); g.arc(320, 300, 160, 0, Math.PI * 2); g.fill(); g.stroke();
      return c;
    }
    g.strokeStyle = "rgba(140, 230, 255, 0.18)"; g.lineWidth = 2;
    for (let x = 0; x < 640; x += 32) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 880); g.stroke(); }
    g.strokeStyle = "#a8f0ff"; g.lineWidth = 6;
    const gearL = (x: number, y: number, r: number, n: number, miss = -1) => {
      g.beginPath();
      for (let i = 0; i <= n * 4; i++) { const a = (i / (n * 4)) * Math.PI * 2, k = Math.floor(i / 2) % 2 && Math.floor(i / 4) !== miss ? r * 1.14 : r; g.lineTo(x + Math.cos(a) * k, y + Math.sin(a) * k); }
      g.closePath(); g.stroke(); g.beginPath(); g.arc(x, y, r * 0.22, 0, Math.PI * 2); g.stroke();
    };
    gearL(380, 360, 170, 22, 5); gearL(170, 560, 110, 14); gearL(210, 250, 70, 10);
    g.strokeStyle = "#ff5a4a"; g.lineWidth = 7; g.beginPath(); g.arc(380 + Math.cos(((5 * 4 + 2) / 88) * Math.PI * 2) * 190, 360 + Math.sin(((5 * 4 + 2) / 88) * Math.PI * 2) * 190, 46, 0, Math.PI * 2); g.stroke();
    g.fillStyle = "#a8f0ff"; g.font = '700 30px "Montserrat", Arial'; g.fillText("SCAN 01", 40, 840);
    return c;
  };
  return { outside: draw(false), inside: draw(true) };
}
