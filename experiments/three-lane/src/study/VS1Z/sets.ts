// REPLICATION STUDY (internal, never published): the places of the VS1Z study built from our own kit pieces.
// Our own geometry and painted textures; the reference is matched only in staging, scale and light, never in design.
//   hallSet()     a stone throne hall: an aisle carpet from the jar to a throne under red drapes, columns and arches,
//                 a round window, candelabras and fire bowls; the jar stands in the aisle
//   jar           a tall bronze vessel with eight gold dragon heads round its shoulder (a ball in each mouth) and eight
//                 stone frogs round its foot, mouths open; dragon i points along DRAGON_AZ[i]
//   balconySet()  a palace balcony (balustrade, banner, carpet) over a parade ground packed with soldiers, a red
//                 runner, a walled city and mountains under a day sky
import * as THREE from "three";
import { NOINK } from "../../ink";
import { SetBuild, lambert, basic, box, cyl, plane, glowSprite, skyDome, makeKey } from "../../kit/sets";
import { stoneCourses } from "../../kit/dressing";
import { brass, tex } from "../../kit/paint2";
import { roundTower, wallRun, house } from "../../kit/architecture";
import { rng } from "../../paint";
import { Flame } from "../../kit/fx";
import type { Rig, V3 } from "../../kit/Stage";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };

// ------------------------------------------------------------------------------------------------ the jar
export const JAR: V3 = [0.4, 0, -0.2];
export const JAR_R = 1.05, JAR_H = 3.05, DRAGON_Y = 1.66, FROG_R = 1.9;
/** dragon azimuths (degrees, from +z toward +x): dragon 0 points to camera-left of the hook framing */
export const DRAGON_AZ = Array.from({ length: 8 }, (_, i) => -36.9 + 45 * i);
const dirOf = (az: number) => [Math.sin((az * Math.PI) / 180), Math.cos((az * Math.PI) / 180)] as const;
/** world position of dragon i's mouth (where its ball sits) */
export const mouthOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); const r = JAR_R + 0.6; return [JAR[0] + sx * r, DRAGON_Y - 0.17, JAR[2] + cz * r]; };
export const headOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); const r = JAR_R + 0.42; return [JAR[0] + sx * r, DRAGON_Y, JAR[2] + cz * r]; };
/** frog i's open mouth */
export const frogMouthOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); return [JAR[0] + sx * FROG_R, 0.5, JAR[2] + cz * FROG_R]; };

const GOLD = () => lambert({ map: brass(), color: "#fff0a8" });
function dragon(gold: THREE.Material): THREE.Group {
  // built pointing +z from the jar wall (local origin on the wall at the dragon's height)
  const g = new THREE.Group();
  const neck = new THREE.CatmullRomCurve3([new THREE.Vector3(0, -0.7, -0.05), new THREE.Vector3(0, -0.2, 0.18), new THREE.Vector3(0, 0.15, 0.3), new THREE.Vector3(0, 0.12, 0.5)]);
  g.add(new THREE.Mesh(new THREE.TubeGeometry(neck, 20, 0.16, 10), gold));
  const skull = new THREE.Mesh(new THREE.SphereGeometry(0.17, 16, 12), gold); skull.scale.set(0.9, 0.8, 1.2); skull.position.set(0, 0.14, 0.5); g.add(skull);
  const upper = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.5, 12), gold); upper.rotation.x = Math.PI / 2 - 0.25; upper.position.set(0, 0.1, 0.8); upper.scale.set(1, 1, 0.6); g.add(upper);
  const nose = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), gold); nose.position.set(0, 0.06, 1.02); g.add(nose);
  const jaw = new THREE.Mesh(new THREE.ConeGeometry(0.08, 0.42, 10), gold); jaw.rotation.x = Math.PI / 2 + 0.75; jaw.position.set(0, -0.12, 0.72); jaw.scale.set(1, 1, 0.5); g.add(jaw);
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 8), lambert({ color: "#4a160f" })); mouth.scale.set(0.9, 0.9, 1.6); mouth.position.set(0, -0.02, 0.72); g.add(mouth);
  for (const sx of [-1, 1]) { const wsk = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(sx * 0.05, 0.05, 0.98), new THREE.Vector3(sx * 0.2, -0.05, 0.9), new THREE.Vector3(sx * 0.28, -0.25, 0.75)]), 8, 0.012, 5), gold); g.add(wsk); }
  for (let k = 0; k < 6; k++) {                                     // spikes along the crest
    const s = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.2 - k * 0.015, 6), gold);
    const u = k / 6; s.position.set(0, 0.3 - u * 0.5, 0.55 - u * 0.65); s.rotation.x = -0.6; g.add(s);
  }
  for (const sx of [-1, 1]) {
    const horn = new THREE.Mesh(new THREE.ConeGeometry(0.03, 0.28, 6), gold); horn.position.set(sx * 0.1, 0.32, 0.42); horn.rotation.set(-0.9, 0, sx * 0.3); g.add(horn);
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), lambert({ color: "#2a1a10" })); eye.position.set(sx * 0.13, 0.17, 0.72); g.add(eye);
  }
  g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return g;
}
function frog(stone: THREE.Material): THREE.Group {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.SphereGeometry(0.34, 16, 12), stone); body.scale.set(1, 0.7, 1.1); body.position.y = 0.24; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.24, 16, 12), stone); head.scale.set(1.15, 0.9, 1); head.position.set(0, 0.42, 0.18); g.add(head);
  const lip = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.035, 8, 20), stone); lip.rotation.x = -Math.PI / 2 + 0.35; lip.position.set(0, 0.56, 0.22); g.add(lip);
  const hole = new THREE.Mesh(new THREE.CircleGeometry(0.12, 18), lambert({ color: "#1d1820" })); hole.rotation.x = -Math.PI / 2 + 0.35; hole.position.set(0, 0.565, 0.22); g.add(hole);
  for (const sx of [-1, 1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8), stone); eye.position.set(sx * 0.15, 0.6, 0.08); g.add(eye);
    const leg = new THREE.Mesh(new THREE.BoxGeometry(0.1, 0.06, 0.36), stone); leg.position.set(sx * 0.32, 0.04, 0.22); leg.rotation.y = sx * 0.5; g.add(leg);
    const back = new THREE.Mesh(new THREE.SphereGeometry(0.14, 10, 8), stone); back.scale.set(0.8, 0.6, 1.4); back.position.set(sx * 0.3, 0.12, -0.12); g.add(back);
  }
  g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return g;
}
export function jar(root: THREE.Object3D) {
  const g = new THREE.Group(); g.position.set(...JAR);
  const prof: [number, number][] = [[0, 0], [1.11, 0], [1.15, 0.1], [1.05, 0.26], [1.0, 0.7], [1.03, 1.4], [1.05, 1.95], [1.01, 2.2], [0.86, 2.42], [0.6, 2.56], [0.57, 2.66], [0.42, 2.76], [0.26, 2.84], [0.16, 2.94], [0.1, 3.02], [0, 3.04]];
  const body = new THREE.Mesh(new THREE.LatheGeometry(prof.map(([r, y]) => new THREE.Vector2(r, y)), 48), lambert({ color: "#666b7e" }));
  body.castShadow = true; body.receiveShadow = true; g.add(body);
  const band = lambert({ color: "#7f8394" });
  for (const [y, r] of [[0.26, 1.06], [2.2, 1.02], [2.56, 0.6]] as [number, number][]) { const b = new THREE.Mesh(new THREE.TorusGeometry(r, 0.035, 8, 64), band); b.rotation.x = Math.PI / 2; b.position.y = y; g.add(b); }
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.16, 14, 10), band); knob.position.y = 3.12; g.add(knob);
  const gold = GOLD(), stone = lambert({ color: "#7f828f" });
  DRAGON_AZ.forEach((az) => {
    const d = dragon(gold); const a = (az * Math.PI) / 180;
    d.position.set(Math.sin(a) * (JAR_R - 0.05), DRAGON_Y, Math.cos(a) * (JAR_R - 0.05)); d.rotation.y = a; d.scale.setScalar(1.12); g.add(d);
    const f = frog(stone); f.position.set(Math.sin(a) * FROG_R, 0, Math.cos(a) * FROG_R); f.rotation.y = a; f.scale.setScalar(0.85); g.add(f);
  });
  root.add(g);
  return g;
}

/** the bronze balls: one per dragon mouth, or a function of time (a falling ball) */
export const ballRig = (pos: (i: number, t: number) => V3 | null, glints = false): Rig => (ctx) => {
  const mat = lambert({ color: "#c47a32" });
  const balls = DRAGON_AZ.map(() => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.085, 16, 12), mat); m.castShadow = true; ctx.root.add(m); return m; });
  void glints;
  return (t) => balls.forEach((m, i) => { const p = pos(i, t); m.visible = !!p; if (p) m.position.set(...p); });
};

// ------------------------------------------------------------------------------------------------ painted textures
function carpet() {
  const [c, g] = canvas(256, 512);
  g.fillStyle = "#26305a"; g.fillRect(0, 0, 256, 512);
  g.fillStyle = "#a3283a"; g.fillRect(0, 0, 22, 512); g.fillRect(234, 0, 22, 512);
  g.fillStyle = "#d9a441"; g.fillRect(24, 0, 6, 512); g.fillRect(226, 0, 6, 512);
  for (let y = 0; y < 512; y += 128) {
    g.strokeStyle = "#a3283a"; g.lineWidth = 10; g.beginPath(); g.moveTo(128, y + 14); g.lineTo(206, y + 64); g.lineTo(128, y + 114); g.lineTo(50, y + 64); g.closePath(); g.stroke();
    g.fillStyle = "#d9a441"; g.beginPath(); g.moveTo(128, y + 46); g.lineTo(150, y + 64); g.lineTo(128, y + 82); g.lineTo(106, y + 64); g.closePath(); g.fill();
  }
  return tex(c, [1, 4]);
}
function roseWindow() {
  const [c, g] = canvas(512, 512), r = rng(5);
  g.fillStyle = "#2b2a44"; g.fillRect(0, 0, 512, 512);
  for (let k = 0; k < 12; k++) {
    const a0 = (k / 12) * Math.PI * 2, a1 = ((k + 1) / 12) * Math.PI * 2;
    for (const [r0, r1] of [[60, 140], [140, 230]]) {
      g.fillStyle = ["#e0b13c", "#c0392b", "#2f6fb5", "#7a4bb0"][Math.floor(r() * 4)];
      g.beginPath(); g.arc(256, 256, r1, a0 + 0.04, a1 - 0.04); g.arc(256, 256, r0, a1 - 0.04, a0 + 0.04, true); g.closePath(); g.fill();
    }
  }
  g.fillStyle = "#f2d27a"; g.beginPath(); g.arc(256, 256, 50, 0, Math.PI * 2); g.fill();
  g.strokeStyle = "#1a1726"; g.lineWidth = 12; g.beginPath(); g.arc(256, 256, 236, 0, Math.PI * 2); g.stroke();
  return tex(c);
}
function drapeTex() {
  const [c, g] = canvas(256, 64);
  for (let x = 0; x < 256; x++) { const v = 0.5 + 0.5 * Math.sin((x / 256) * Math.PI * 12); g.fillStyle = `rgb(${Math.round(120 + 70 * v)}, ${Math.round(24 + 18 * v)}, ${Math.round(34 + 16 * v)})`; g.fillRect(x, 0, 1, 64); }
  return tex(c);
}
function tufted() {
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#b8302f"; g.fillRect(0, 0, 256, 256);
  g.fillStyle = "#e3a640";
  for (let y = 16; y < 256; y += 32) for (let x = (y / 32) % 2 ? 32 : 16; x < 256; x += 32) { g.beginPath(); g.arc(x, y, 3.5, 0, Math.PI * 2); g.fill(); }
  return tex(c, [2, 3]);
}
function shield() {
  const [c, g] = canvas(128, 160);
  g.fillStyle = "#2f63b5"; g.beginPath(); g.moveTo(8, 8); g.lineTo(120, 8); g.lineTo(120, 90); g.quadraticCurveTo(64, 160, 64, 156); g.quadraticCurveTo(8, 130, 8, 90); g.closePath(); g.fill();
  g.strokeStyle = "#e3a640"; g.lineWidth = 8; g.stroke();
  g.fillStyle = "#f2d27a"; g.beginPath(); g.moveTo(40, 40); g.lineTo(88, 40); g.lineTo(64, 110); g.closePath(); g.fill();
  return tex(c);
}

// ------------------------------------------------------------------------------------------------ the throne hall
export const THRONE_Z = -13.2, DAIS_Y = 0.5;
export const EMPEROR: V3 = [0, DAIS_Y, THRONE_Z + 0.9];
export const GUARDS: V3[] = [[-0.85, DAIS_Y, THRONE_Z + 0.6], [0.85, DAIS_Y, THRONE_Z + 0.6]];

export function hallSet(): SetBuild & { flames: Flame[]; flameAt: V3[] } {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  const stoneWall = lambert({ map: stoneCourses([3, 3], { hue: 34, light: 56, seed: 11 }), color: "#c4b8ae" });
  const floor = lambert({ map: stoneCourses([10, 14], { hue: 30, light: 44, seed: 3 }), color: "#9a8f88" });
  plane(root, floor, 22, 40, 0, 0, -6, -Math.PI / 2);
  box(root, lambert({ map: carpet() }), 2.6, 0.02, 17, 0, 0.012, THRONE_Z + 8.4, false);
  // columns and arches down both sides, a clerestory of arched windows above
  const col = lambert({ color: "#b8ab9c" }), gold = GOLD();
  for (let z = 5; z > -15; z -= 3.6) for (const s of [-1, 1]) {
    cyl(root, col, 0.42, 7.5, s * 5.0, 3.75, z, 18);
    box(root, col, 1.1, 0.5, 1.1, s * 5.0, 0.25, z); box(root, col, 1.1, 0.4, 1.1, s * 5.0, 7.6, z);
    const a = new THREE.Mesh(new THREE.TorusGeometry(1.8, 0.28, 8, 24, Math.PI), col); a.position.set(s * 5.0, 7.8, z - 1.8); a.rotation.y = Math.PI / 2; a.castShadow = true; root.add(a);
  }
  for (const s of [-1, 1]) {
    box(root, stoneWall, 0.4, 14, 40, s * 8.0, 7, -6, true, 2);
    for (let z = 4; z > -15; z -= 3.6) {
      const win = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 3.2), basic({ color: "#f7e2b0" })); win.position.set(s * 7.78, 5.2, z); win.rotation.y = -s * Math.PI / 2; win.layers.set(NOINK); root.add(win);
      glows.push(glowSprite(root, [255, 220, 160], 3.2, s * 7.4, 5.2, z));
    }
  }
  box(root, stoneWall, 16, 15, 0.4, 0, 7.5, THRONE_Z - 3.4, true, 2);                   // back wall
  box(root, lambert({ color: "#3b3352" }), 16, 0.4, 40, 0, 14.5, -6);                  // ceiling
  const rose = new THREE.Mesh(new THREE.CircleGeometry(1.9, 40), basic({ map: roseWindow() })); rose.position.set(0, 10.2, THRONE_Z - 3.18); rose.layers.set(NOINK); root.add(rose);
  glows.push(glowSprite(root, [255, 200, 150], 5, 0, 10.2, THRONE_Z - 2.9));
  // dais, drapes, valance, throne
  box(root, lambert({ color: "#8e8aa8" }), 6, 0.25, 4, 0, 0.125, THRONE_Z + 0.4);
  box(root, lambert({ color: "#8e8aa8" }), 5, 0.25, 3.4, 0, 0.375, THRONE_Z + 0.1);
  box(root, lambert({ map: carpet() }), 2.6, 0.02, 2.6, 0, 0.51, THRONE_Z + 0.6, false);
  const drape = lambert({ map: drapeTex() });
  for (const s of [-1, 1]) box(root, drape, 0.9, 7.0, 0.25, s * 2.0, 3.5, THRONE_Z - 1.2);
  box(root, lambert({ map: tufted() }), 2.4, 5.5, 0.2, 0, 3.1, THRONE_Z - 1.5);
  box(root, drape, 5, 0.8, 0.35, 0, 7.1, THRONE_Z - 1.0); box(root, gold, 5.1, 0.16, 0.4, 0, 6.66, THRONE_Z - 0.95);
  const tb = new THREE.Group(); tb.position.set(0, DAIS_Y, THRONE_Z - 0.3); root.add(tb);
  box(tb, lambert({ map: tufted() }), 1.5, 2.6, 0.18, 0, 1.6, -0.05);
  for (const s of [-1, 1]) { box(tb, gold, 0.16, 3.2, 0.2, s * 0.85, 1.6, 0); const sp = new THREE.Mesh(new THREE.ConeGeometry(0.12, 0.6, 8), gold); sp.position.set(s * 0.85, 3.5, 0); tb.add(sp); }
  box(tb, gold, 1.86, 0.18, 0.22, 0, 2.95, 0); const peak = new THREE.Mesh(new THREE.ConeGeometry(0.5, 1.0, 4), gold); peak.position.set(0, 3.5, 0); peak.rotation.y = Math.PI / 4; tb.add(peak);
  box(tb, gold, 1.8, 0.5, 0.9, 0, 0.45, 0.4); box(tb, lambert({ color: "#b8302f" }), 1.5, 0.12, 0.8, 0, 0.75, 0.42);
  const sh = new THREE.Mesh(new THREE.PlaneGeometry(0.5, 0.62), lambert({ map: shield(), transparent: true })); sh.position.set(0, 2.3, 0.05); tb.add(sh);
  // candelabras down the aisle and fire bowls near the jar (practicals)
  const flames: Flame[] = [], flameAt: V3[] = [];
  const iron = lambert({ color: "#3a3446" });
  const candle = (x: number, y: number, z: number) => {
    cyl(root, lambert({ color: "#f3ecd8" }), 0.035, 0.22, x, y + 0.11, z, 8);
    const f = new THREE.Mesh(new THREE.SphereGeometry(0.035, 8, 6), basic({ color: "#ffd27a" })); f.position.set(x, y + 0.27, z); f.layers.set(NOINK); f.userData.bloom = true; root.add(f);
  };
  for (const z of [-3.5, -7.5, -11]) for (const s of [-1, 1]) {
    const x = s * 2.9; cyl(root, gold, 0.04, 2.1, x, 1.05, z, 8); box(root, gold, 0.9, 0.05, 0.05, x, 2.1, z);
    for (const dx of [-0.42, -0.21, 0, 0.21, 0.42]) candle(x + dx, 2.1 + (dx === 0 ? 0.15 : 0), z);
    glows.push(glowSprite(root, [255, 200, 120], 2.2, x, 2.3, z));
  }
  for (const [x, z] of [[-3.2, -1.5], [3.4, -3.0], [-3.4, 2.5]] as [number, number][]) {
    cyl(root, iron, 0.06, 1.0, x, 0.5, z, 8);
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.3, 0.3, 16), iron); bowl.position.set(x, 1.1, z); bowl.castShadow = true; root.add(bowl);
    const fl = new Flame(0.9, x + z); fl.mesh.position.set(x, 1.2, z); root.add(fl.mesh); flames.push(fl); flameAt.push([x, 1.2, z]);
    glows.push(glowSprite(root, [255, 170, 80], 3.0, x, 1.6, z));
  }
  jar(root);
  const key = makeKey(root, [-9, 13, 7], [0, 0, -4], 16);
  return { root, key, glows, extra: {}, flames, flameAt };
}
/** fire bowls flicker (rig) */
export const flamesRig = (): Rig => (ctx) => {
  const s = ctx.set as ReturnType<typeof hallSet>;
  return (t, cam) => s.flames.forEach((f) => f.update(t, 1, cam));
};

// ------------------------------------------------------------------------------------------------ the balcony
export const BAL_EMP: V3 = [0, 0, 0];
export function balconySet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  skyDome(root, "#3f86d6", "#8cc0ec", "#e6eef2");
  const stone = lambert({ color: "#ece6dc" });
  // balcony floor with a red carpet, a balustrade behind the emperor
  box(root, stone, 14, 0.4, 6, 0, -0.2, 0.5);
  box(root, lambert({ color: "#a52a2a" }), 3.2, 0.02, 4, 0, 0.012, 0.8, false);
  box(root, lambert({ color: "#e0b040" }), 3.4, 0.015, 4.2, 0, 0.008, 0.8, false);
  const BZ = -1.3;
  box(root, stone, 14, 0.18, 0.5, 0, 1.05, BZ); box(root, stone, 14, 0.14, 0.42, 0, 0.07, BZ);
  for (let x = -6.8; x <= 6.8; x += 0.32) {
    const b = new THREE.Mesh(new THREE.LatheGeometry([[0.0, 0], [0.09, 0.02], [0.06, 0.2], [0.11, 0.5], [0.05, 0.8], [0.08, 0.95], [0, 0.96]].map(([r, y]) => new THREE.Vector2(r, y)), 10), stone);
    b.position.set(x, 0.1, BZ); b.castShadow = true; root.add(b);
  }
  for (const x of [-3.2, 3.2]) box(root, stone, 0.6, 1.3, 0.6, x, 0.65, BZ);
  // a stone griffin-less urn on the right post, a banner pole on the left
  const urn = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.25, 0.05], [0.35, 0.35], [0.2, 0.6], [0.3, 0.75], [0, 0.78]].map(([r, y]) => new THREE.Vector2(r, y)), 16), lambert({ color: "#d9cbb0" }));
  urn.position.set(3.2, 1.3, BZ); urn.castShadow = true; root.add(urn);
  cyl(root, lambert({ color: "#5a3a2a" }), 0.05, 4.2, -2.6, 2.1, 1.2, 8);
  const ban = box(root, lambert({ color: "#8a2236" }), 0.9, 2.2, 0.04, -2.15, 2.7, 1.2); void ban;
  box(root, lambert({ color: "#e0b040" }), 0.95, 0.08, 0.06, -2.15, 3.8, 1.2);
  // the parade ground below (y -14): two blocks of soldiers either side of a red runner, the city beyond
  const GY = -14;
  plane(root, lambert({ color: "#c9b892" }), 220, 260, 0, GY, -110, -Math.PI / 2);
  box(root, lambert({ color: "#b22a2a" }), 3, 0.05, 160, 0, GY + 0.03, -86, false);
  for (let z = -10; z > -160; z -= 9) for (const s of [-1, 1]) { cyl(root, lambert({ color: "#7a2a3a" }), 0.08, 3.2, s * 2.4, GY + 1.6, z, 6); box(root, lambert({ color: "#b8343a" }), 0.6, 1.4, 0.04, s * 2.4 + s * 0.32, GY + 2.4, z); }
  // soldiers: instanced bodies, heads and helmets (rows of 3 m depth)
  const pos: [number, number][] = [];
  for (let z = -12; z > -150; z -= 1.3) for (const s of [-1, 1]) for (let x = 2.4; x < 60; x += 1.1) pos.push([s * x, z]);
  const n = pos.length, m4 = new THREE.Matrix4();
  const bodies = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.28, 0.36, 1.2, 8), lambert({ color: "#6e2836" }), n);
  const heads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.24, 10, 8), lambert({ color: "#f2efe8" }), n);
  const helms = new THREE.InstancedMesh(new THREE.SphereGeometry(0.26, 10, 6, 0, Math.PI * 2, 0, Math.PI / 2), lambert({ color: "#8e95a6" }), n);
  const r = rng(9);
  pos.forEach(([x, z], i) => {
    const j = (r() - 0.5) * 0.12;
    m4.makeTranslation(x + j, GY + 0.6, z); bodies.setMatrixAt(i, m4);
    m4.makeTranslation(x + j, GY + 1.42, z); heads.setMatrixAt(i, m4);
    m4.makeTranslation(x + j, GY + 1.5, z); helms.setMatrixAt(i, m4);
  });
  for (const im of [bodies, heads, helms]) { im.castShadow = true; im.receiveShadow = true; root.add(im); }
  // the city: walls and towers round the parade ground, houses beyond, mountains far
  const wall = (len: number, x: number, z: number, ry: number) => { const w = wallRun(len, 9, 3, 5); w.position.set(x, GY, z); w.rotation.y = ry; root.add(w); };
  wall(130, 0, -165, 0); wall(150, -64, -90, Math.PI / 2); wall(150, 64, -90, Math.PI / 2);
  for (const [x, z] of [[-64, -165], [64, -165], [-18, -165], [18, -165], [-64, -20], [64, -20]] as [number, number][]) { const t = roundTower(4, 20, 3); t.position.set(x, GY, z); root.add(t); }
  for (const s of [-1, 1]) for (let z = -20; z > -160; z -= 12) { box(root, lambert({ color: "#e9e1d4" }), 10, 16, 8, s * 56, GY + 8, z); box(root, lambert({ color: "#5d6a9a" }), 10.6, 3, 8.6, s * 56, GY + 17.5, z); }
  const rr = rng(4);
  for (let k = 0; k < 60; k++) { const h = house({ w: 5 + rr() * 4, h: 5 + rr() * 6, d: 5, seed: k }); h.position.set((rr() - 0.5) * 220, GY, -185 - rr() * 70); root.add(h); }
  const mt = lambert({ color: "#9fb0cf" });
  for (let k = 0; k < 14; k++) { const c = new THREE.Mesh(new THREE.ConeGeometry(40 + rr() * 30, 70 + rr() * 50, 6), mt); c.position.set(-260 + k * 40 + rr() * 20, GY + 20, -330 - rr() * 60); root.add(c); }
  const key = makeKey(root, [-30, 40, 30], [0, GY, -50], 120);
  return { root, key, glows, extra: {}, fogScale: 6 };
}
