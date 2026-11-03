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
import { stoneCourses, clouds } from "../../kit/dressing";
import { tex } from "../../kit/paint2";
import { metal, reliefNormal, grainNormal } from "../../kit/materials";
import { dragonHead, vessel, toad, orb } from "../../kit/heroprops";
import { stoneMat, arcade, archway, roseWindow, banner, throne, carpet, candelabra } from "../../kit/interior";
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
// round 3 (visual track): the dragons are kit/heroprops.ts sculpted heads in real gold, origin at r JAR_R + 0.25
const D_R = JAR_R + 0.28, D_Y = DRAGON_Y + 0.15, D_S = 0.72;   // big, readable heads at the shoulder, as on screen in the master
export const mouthOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); const r = D_R + 0.29; return [JAR[0] + sx * r, D_Y - 0.11, JAR[2] + cz * r]; };
export const headOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); const r = D_R + 0.2; return [JAR[0] + sx * r, D_Y + 0.04, JAR[2] + cz * r]; };
/** frog i's open mouth */
export const frogMouthOf = (i: number): V3 => { const [sx, cz] = dirOf(DRAGON_AZ[i]); const r = FROG_R - 0.25; return [JAR[0] + sx * r, 0.37, JAR[2] + cz * r]; };

export function jar(root: THREE.Object3D) {
  const g = new THREE.Group(); g.position.set(...JAR);
  const prof: [number, number][] = [[0, 0], [1.11, 0], [1.15, 0.1], [1.05, 0.26], [1.0, 0.7], [1.03, 1.4], [1.05, 1.95], [1.01, 2.2], [0.86, 2.42], [0.6, 2.56], [0.57, 2.66], [0.42, 2.76], [0.26, 2.84], [0.16, 2.94], [0.1, 3.02], [0, 3.04]];
  const greyBody = new THREE.MeshStandardMaterial({ color: "#e2eaf8", metalness: 0, roughness: 0.75, normalMap: grainNormal(9) });   // the master's jar reads pale grey-white on screen greyBody.userData.env = true;
  const greyBand = new THREE.MeshStandardMaterial({ color: "#cad2e2", metalness: 0, roughness: 0.6, normalMap: reliefNormal() }); greyBand.userData.env = true;
  g.add(vessel(prof, { body: greyBody, band: greyBand, bands: [[0.4, 1.04], [1.05, 1.0], [2.1, 1.03]], knob: 0.17 }));   // the master's jar reads light grey with gold dragons
  const gold = metal("gold", { scales: 10, repeat: [3, 2] }), toadMat = new THREE.MeshStandardMaterial({ color: "#a8aab2", metalness: 0.2, roughness: 0.6, normalMap: grainNormal(5) });
  DRAGON_AZ.forEach((az, i) => {
    const a = (az * Math.PI) / 180;
    const d = dragonHead({ mat: gold, seed: i, open: 0.6 }); d.scale.setScalar(D_S);
    d.position.set(Math.sin(a) * D_R, D_Y, Math.cos(a) * D_R); d.rotation.y = a; d.rotateX(0.12); g.add(d);
    const f = toad({ mat: toadMat }); f.position.set(Math.sin(a) * FROG_R, 0, Math.cos(a) * FROG_R); f.rotation.y = a + Math.PI; f.scale.setScalar(0.85); g.add(f);
  });
  root.add(g);
  return g;
}

/** the bronze balls: one per dragon mouth, or a function of time (a falling ball) */
export const ballRig = (pos: (i: number, t: number) => V3 | null): Rig => (ctx) => {
  const balls = DRAGON_AZ.map(() => { const m = orb("bronze", 0.085); ctx.root.add(m); return m; });
  return (t) => balls.forEach((m, i) => { const p = pos(i, t); m.visible = !!p; if (p) m.position.set(...p); });
};

// ------------------------------------------------------------------------------------------------ painted textures
function drapeTex() {
  const [c, g] = canvas(256, 64);
  for (let x = 0; x < 256; x++) { const v = 0.5 + 0.5 * Math.sin((x / 256) * Math.PI * 12); g.fillStyle = `rgb(${Math.round(120 + 70 * v)}, ${Math.round(24 + 18 * v)}, ${Math.round(34 + 16 * v)})`; g.fillRect(x, 0, 1, 64); }
  return tex(c);
}

// ------------------------------------------------------------------------------------------------ the throne hall
export const THRONE_Z = -13.2, DAIS_Y = 0.5;
export const EMPEROR: V3 = [0, DAIS_Y, THRONE_Z + 0.9];
export const GUARDS: V3[] = [[-0.85, DAIS_Y, THRONE_Z + 0.6], [0.85, DAIS_Y, THRONE_Z + 0.6]];

export function hallSet(): SetBuild & { flames: Flame[]; flameAt: V3[]; lights: V3[] } {
  // round 3 (visual track): built from kit/interior.ts in warm candle-lit stone (lesson 2), real gold, a carved throne,
  // banners, a rose window, candelabras whose flames feed the bloom and the bokeh discs (lights)
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [], lights: V3[] = [];
  const stone = stoneMat({ light: 72, hue: 255 }), stoneDark = stoneMat({ light: 58, hue: 250, seed: 4 });   // grey-lavender stone (VS1Z)
  const pale = lambert({ color: "#d4ccd0" });
  const floor = lambert({ map: stoneCourses([10, 14], { hue: 230, light: 58, seed: 3 }), color: "#b8b4c4" });
  plane(root, floor, 22, 40, 0, 0, -6, -Math.PI / 2);
  const run = carpet(2.6, 17, { field: "#2c3a6a", border: "#9a2230", accent: "#e0a840" }); run.position.z = THRONE_Z + 8.4; root.add(run);
  arcade(root, { x: 5.0, z0: 5, z1: -15, step: 3.6, h: 7.0, mat: pale, gold: true });
  for (const sx of [-1, 1]) {
    box(root, stone, 0.4, 14, 40, sx * 8.0, 7, -6, true, 2.5);
    for (let z = 3.2; z > -15; z -= 3.6) {
      const ar = archway(1.4, 3.6, { depth: 0.3, mat: stoneDark }); ar.position.set(sx * 7.78, 3.4, z); ar.rotation.y = -sx * Math.PI / 2; root.add(ar);
      const win = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 3.0), basic({ color: "#ffd9a0" })); (win.material as THREE.MeshBasicMaterial).color.multiplyScalar(1.3);
      win.position.set(sx * 7.76, 5.2, z); win.rotation.y = -sx * Math.PI / 2; win.layers.set(NOINK); win.userData.bloom = true; root.add(win);
      glows.push(glowSprite(root, [255, 200, 130], 3.0, sx * 7.3, 5.2, z));
      const bn = banner(1.0, 2.6, { color: ["#9a2230", "#2a4a8a"][Math.abs(Math.round(z)) % 2], emblem: "#e3b448", seed: Math.round(z) }); bn.position.set(sx * 7.7, 9.6, z - 1.8); bn.rotation.y = -sx * Math.PI / 2; root.add(bn);
      // wall sconces between the windows
      const cz = z - 1.8, c = candelabra({ n: 3, h: 0.5, spread: 0.18 }); c.position.set(sx * 7.6, 2.6, cz); c.rotation.y = -sx * Math.PI / 2; root.add(c);
      lights.push([sx * 7.55, 3.1, cz]);
    }
  }
  box(root, stone, 16, 15, 0.4, 0, 7.5, THRONE_Z - 3.4, true, 2.5);                   // back wall
  box(root, lambert({ color: "#2a1c16" }), 16, 0.4, 40, 0, 14.5, -6);                  // ceiling, lost in the dark
  for (let z = 5; z > -16; z -= 3.6) box(root, lambert({ color: "#3a2618" }), 16, 0.5, 0.5, 0, 14.0, z);   // beams
  const rose = roseWindow(1.9, { mat: pale }); rose.position.set(0, 10.4, THRONE_Z - 3.18); root.add(rose);
  glows.push(glowSprite(root, [255, 190, 130], 5, 0, 10.4, THRONE_Z - 2.9));
  const back = archway(5.4, 9.0, { depth: 0.6, band: 0.6, mat: pale }); back.position.set(0, 0, THRONE_Z - 3.0); root.add(back);
  // dais, drapes, valance, throne
  box(root, stoneDark, 6, 0.25, 4, 0, 0.125, THRONE_Z + 0.4);
  box(root, stone, 5, 0.25, 3.4, 0, 0.375, THRONE_Z + 0.1);
  const dc = carpet(2.6, 2.6, { field: "#2c3a6a", border: "#9a2230", accent: "#e0a840" }); dc.position.set(0, 0.5, THRONE_Z + 0.6); root.add(dc);
  const drape = lambert({ map: drapeTex() });
  for (const sx of [-1, 1]) box(root, drape, 0.9, 7.0, 0.25, sx * 2.0, 3.5, THRONE_Z - 1.2);
  box(root, drape, 5, 0.8, 0.35, 0, 7.1, THRONE_Z - 1.0); box(root, metal("gold", { grain: true }), 5.1, 0.16, 0.4, 0, 6.66, THRONE_Z - 0.95);
  const th = throne({ wood: metal("gold", { grain: true, rough: 0.42 }), cushion: "#b8302f" }); th.position.set(0, DAIS_Y, THRONE_Z - 0.4); root.add(th);
  // candelabras down the aisle and fire bowls near the jar (practicals)
  const flames: Flame[] = [], flameAt: V3[] = [];
  for (const z of [-3.5, -7.5, -11]) for (const sx of [-1, 1]) {
    const x = sx * 2.9, c = candelabra({ n: 5, h: 2.1 }); c.position.set(x, 0, z); root.add(c);
    for (const f of c.flames) lights.push([x + f[0], f[1], z + f[2]]);
    glows.push(glowSprite(root, [255, 196, 110], 2.4, x, 2.4, z));
  }
  const iron = metal("iron", { grain: true });
  for (const [x, z] of [[-3.2, -1.5], [3.4, -3.0], [-3.4, 2.5]] as [number, number][]) {
    cyl(root, iron, 0.06, 1.0, x, 0.5, z, 8);
    const bowl = new THREE.Mesh(new THREE.CylinderGeometry(0.55, 0.3, 0.3, 24), iron); bowl.position.set(x, 1.1, z); bowl.castShadow = true; root.add(bowl);
    const fl = new Flame(0.9, x + z); fl.mesh.position.set(x, 1.2, z); root.add(fl.mesh); flames.push(fl); flameAt.push([x, 1.2, z]);
    glows.push(glowSprite(root, [255, 170, 80], 3.2, x, 1.6, z));
    for (const [dx, dz] of [[0, 0], [0.3, 0.1], [-0.25, -0.15]]) lights.push([x + dx, 1.45, z + dz]);
  }
  jar(root);
  const key = makeKey(root, [-9, 13, 7], [0, 0, -4], 16);
  return { root, key, glows, extra: {}, flames, flameAt, lights };
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
  wall(130, 0, -165, 0); wall(150, -64, -90, Math.PI / 2);   // (round 3) the far wall stays; the town now fills behind it
  wall(150, 64, -90, Math.PI / 2);
  for (const [x, z] of [[-64, -165], [64, -165], [-18, -165], [18, -165], [-64, -20], [64, -20]] as [number, number][]) { const t = roundTower(4, 20, 3); t.position.set(x, GY, z); root.add(t); }
  for (const s of [-1, 1]) for (let z = -20; z > -160; z -= 12) { box(root, lambert({ color: "#e9e1d4" }), 10, 16, 8, s * 56, GY + 8, z); box(root, lambert({ color: "#5d6a9a" }), 10.6, 3, 8.6, s * 56, GY + 17.5, z); }
  const rr = rng(4);
  for (let k = 0; k < 140; k++) { const h = house({ w: 5 + rr() * 4, h: 5 + rr() * 6, d: 5, seed: k, base: ["#f4efe6", "#ece4d6", "#f7f2ea"][k % 3] }); h.position.set((rr() - 0.5) * 220, GY, -185 - rr() * 70); root.add(h); }   // round 3: a white town (the reference's city reads white under mountains)
  const mt = lambert({ color: "#9fb0cf" });
  const snow = lambert({ color: "#f4f6fa" });
  for (let k = 0; k < 14; k++) { const hh = 90 + rr() * 60, rad = 50 + rr() * 30, c = new THREE.Mesh(new THREE.ConeGeometry(rad, hh, 7), mt); c.position.set(-260 + k * 40 + rr() * 20, GY + hh / 2 - 10, -330 - rr() * 60); root.add(c);
    const cap = new THREE.Mesh(new THREE.ConeGeometry(rad * 0.3, hh * 0.3, 7), snow); cap.position.set(c.position.x, c.position.y + hh * 0.35 + 0.5, c.position.z); root.add(cap); }
  clouds(root, { n: 14, x: [-260, 260], y: [60, 140], z: [-420, -260], size: 70, seed: 3 });   // round 3 (judge: "a plain gradient sky")
  const key = makeKey(root, [-30, 40, 30], [0, GY, -50], 120);
  return { root, key, glows, extra: {}, fogScale: 6 };
}
