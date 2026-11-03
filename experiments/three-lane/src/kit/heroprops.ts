// Hero props (our own code and geometry; visual track round 3, replication lesson 1). Sculpted procedurally, in
// real metal / glaze materials (kit/materials.ts), so a close-up of a story's key object reads as a crafted thing:
// deformed and displaced surfaces instead of bare spheres and cones, tapered horns and whiskers, rows of teeth, a
// flame-like mane, cast scales. No third-party geometry, so nothing to license (logged in public/models/LICENSES.md).
//   dragonHead(o)          a coiling Chinese dragon head and neck, built pointing +z from its origin (mouth open)
//   vessel(profile, o)     a lathed vessel (bronze jar, vase) with cast relief bands and a lid
//   toad(o)                a squat toad with an open mouth, bumpy skin, gaze up
//   orb(kind, r)           a metal ball (bronze, gold)
import * as THREE from "three";
import { metal, glaze, type MetalKind } from "./materials";
import { rng } from "../paint";

const V = (x: number, y: number, z: number) => new THREE.Vector3(x, y, z);
const shadowed = (g: THREE.Object3D) => { g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };

/** a tube along a curve whose radius follows r(u) (u 0..1) - horns, whiskers, necks, tails */
export function taperTube(curve: THREE.Curve<THREE.Vector3>, r: (u: number) => number, seg = 32, radial = 10, mat?: THREE.Material): THREE.Mesh {
  const geo = new THREE.TubeGeometry(curve, seg, 1, radial, false);
  const pos = geo.getAttribute("position") as THREE.BufferAttribute, c = new THREE.Vector3(), p = new THREE.Vector3();
  for (let i = 0; i <= seg; i++) {
    const u = i / seg; curve.getPointAt(u, c); const k = r(u);
    for (let j = 0; j <= radial; j++) { const idx = i * (radial + 1) + j; p.fromBufferAttribute(pos, idx).sub(c).multiplyScalar(k).add(c); pos.setXYZ(idx, p.x, p.y, p.z); }
  }
  pos.needsUpdate = true; geo.computeVertexNormals();
  return new THREE.Mesh(geo, mat);
}

/** a sphere deformed vertex by vertex: f maps a unit-sphere point to its new place */
function sculpt(f: (p: THREE.Vector3) => THREE.Vector3, w = 48, h = 32): THREE.BufferGeometry {
  const geo = new THREE.SphereGeometry(1, w, h), pos = geo.getAttribute("position") as THREE.BufferAttribute, p = new THREE.Vector3();
  for (let i = 0; i < pos.count; i++) { p.fromBufferAttribute(pos, i); const q = f(p.clone()); pos.setXYZ(i, q.x, q.y, q.z); }
  geo.computeVertexNormals(); return geo;
}
const bump = (x: number, c: number, w: number) => Math.exp(-((x - c) * (x - c)) / (w * w));

/** flame-like mane tuft: a flattened curved cone */
function tuft(mat: THREE.Material, len: number, curl: number): THREE.Mesh {
  const c = new THREE.QuadraticBezierCurve3(V(0, 0, 0), V(0, len * 0.55, -len * 0.25), V(0, len * (0.9 - curl * 0.3), -len * (0.55 + curl)));
  const m = taperTube(c, (u) => 0.22 * len * (1 - u) ** 1.3 + 0.004, 12, 7, mat); m.scale.x = 0.45; return m;
}

export type DragonOpts = { mat?: THREE.Material; headMat?: THREE.Material; open?: number; neck?: boolean; seed?: number; tongue?: boolean };
/** a Chinese dragon head (mouth open, pointing +z, about 0.9 m nose to mane at scale 1) on an S-curved scaled neck.
 * Features (eyes, brows, horns, whiskers, mane, teeth) are snapped onto the sculpted skull by raycasting, so they sit
 * on its surface whatever the sculpt's proportions. */
export function dragonHead(o: DragonOpts = {}): THREE.Group {
  const g = new THREE.Group(), r = rng(o.seed ?? 4);
  const scaleGold = o.mat ?? metal("gold", { scales: 10, repeat: [3, 2] });
  const gold = o.headMat ?? metal("gold", { scales: 16, repeat: [4, 3] }), goldFine = metal("gold", { grain: true });
  const mouthMat = new THREE.MeshStandardMaterial({ color: "#5a1410", roughness: 0.7 });
  const toothMat = glaze("#f4ead2", { rough: 0.3 }), eyeMat = glaze("#f1d36a", { rough: 0.15 }), pupilMat = glaze("#1a1010", { rough: 0.1 });
  const open = o.open ?? 0.7;
  // the skull: a bulky cranium, a shorter blunt snout, heavy brow ridges, a raised nose pad, a flat jawline underneath
  const skull = new THREE.Mesh(sculpt((p) => {
    const fwd = Math.max(0, p.z), zf = p.z > 0 ? 1.75 : 0.85;   // a long snout (judge: "frog-like" at 1.45)
    const y = p.y > 0 ? p.y * (1.0 - 0.38 * fwd) : p.y * 0.32;
    const brow = 0.28 * bump(p.z, 0.0, 0.28) * Math.max(0, p.y - 0.2) * bump(Math.abs(p.x), 0.45, 0.3);
    const nose = 0.22 * bump(p.z, 0.85, 0.18) * Math.max(0, p.y + 0.1);
    const cheek = 0.16 * bump(p.y, -0.05, 0.3) * bump(p.z, -0.1, 0.4);
    const ridge = 0.04 * Math.sin(p.z * 18) * Math.max(0, p.y) * (p.z > 0.1 && p.z < 0.8 ? 1 : 0);
    return V(p.x * 0.5 * (1 - 0.32 * fwd) * (1 + cheek), (y + brow + nose + ridge) * 0.5, p.z * 0.5 * zf);
  }, 64, 40), gold);
  g.add(skull); skull.updateMatrixWorld(true);
  const ray = new THREE.Raycaster(), C = V(0, 0.08, 0);
  /** the skull surface point and normal along a direction from the head's centre */
  const on = (dir: THREE.Vector3, from = C): { p: THREE.Vector3; n: THREE.Vector3 } => {
    const d = dir.clone().normalize(); ray.set(from.clone().addScaledVector(d, 2), d.clone().negate());
    const hit = ray.intersectObject(skull, false)[0];
    if (!hit) return { p: from.clone().addScaledVector(d, 0.3), n: d };
    return { p: hit.point.clone(), n: (hit.face?.normal.clone() ?? d) };
  };
  // lower jaw, hinged at the back, opened by `open`
  const jaw = new THREE.Group(); jaw.position.set(0, -0.06, -0.12); jaw.rotation.x = open * 0.75; g.add(jaw);
  const jawM = new THREE.Mesh(sculpt((p) => { const zf = p.z > 0 ? 1.35 : 0.5, taper = 1 - 0.38 * Math.max(0, p.z); return V(p.x * 0.42 * taper, (p.y > 0 ? p.y * 0.07 : p.y * 0.24), p.z * 0.5 * zf); }), gold);
  jawM.position.z = 0.16; jaw.add(jawM);
  const lining = new THREE.Mesh(sculpt((p) => V(p.x * 0.36 * (1 - 0.35 * Math.max(0, p.z)), p.y * 0.1, p.z * 0.42 * (p.z > 0 ? 1.4 : 0.5))), mouthMat);
  lining.position.set(0, -0.08, 0.1); g.add(lining);
  if (o.tongue !== false) { const tg = taperTube(new THREE.CatmullRomCurve3([V(0, 0.03, 0.05), V(0, 0.06, 0.3), V(0, 0.03, 0.5), V(0, 0.1, 0.62)]), (u) => 0.055 * (1 - u * 0.7), 16, 8, new THREE.MeshStandardMaterial({ color: "#c0453a", roughness: 0.5 })); tg.scale.x = 1.6; jaw.add(tg); }
  // teeth along the upper jaw's edge (snapped) and the lower jaw, a fang pair each side
  for (const s of [-1, 1]) for (let k = 0; k < 6; k++) {
    const z = 0.12 + k * 0.1, e = on(V(s, 0, 0), V(0, -0.1, z));
    const up = new THREE.Mesh(new THREE.ConeGeometry(0.024, k === 0 ? 0.17 : 0.075, 6), toothMat); up.position.copy(e.p).add(V(-s * 0.03, -0.02, 0)); up.rotation.x = Math.PI; g.add(up);
    const lo = new THREE.Mesh(new THREE.ConeGeometry(0.022, k === 1 ? 0.15 : 0.065, 6), toothMat); lo.position.set(s * (0.17 - k * 0.018), 0.04, 0.12 + z * 0.95); jaw.add(lo);
  }
  // eyes: bulging gold-yellow with black slit pupils, under brow ridges
  for (const s of [-1, 1]) {
    const e = on(V(s * 0.7, 0.62, 0.3));
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.055, 16, 12), eyeMat); eye.position.copy(e.p).addScaledVector(e.n, 0.01); g.add(eye);
    const pupil = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 8), pupilMat); pupil.scale.set(0.5, 1.2, 0.6); pupil.position.copy(e.p).addScaledVector(e.n, 0.07); g.add(pupil);
    const b = on(V(s * 0.6, 0.85, 0.22));
    const brow = taperTube(new THREE.CatmullRomCurve3([b.p.clone().add(V(-s * 0.08, -0.02, 0.06)), b.p.clone().add(V(0, 0.03, 0)), b.p.clone().add(V(s * 0.08, 0.02, -0.08))]), (u) => 0.035 * Math.sin(Math.PI * (0.15 + 0.7 * u)), 12, 8, goldFine); g.add(brow);
  }
  // horns: tapered, swept back and up with a curl, from the top of the skull
  for (const s of [-1, 1]) {
    const h0 = on(V(s * 0.35, 1, -0.35)).p;
    const c = new THREE.CatmullRomCurve3([h0.clone().add(V(0, -0.03, 0)), h0.clone().add(V(s * 0.08, 0.2, -0.2)), h0.clone().add(V(s * 0.14, 0.32, -0.5)), h0.clone().add(V(s * 0.1, 0.5, -0.7))]);
    g.add(taperTube(c, (u) => 0.065 * (1 - u) + 0.007, 24, 10, goldFine));
    const t = c.getPointAt(0.35); g.add(taperTube(new THREE.LineCurve3(t, t.clone().add(V(s * 0.08, 0.1, 0.03))), (u) => 0.022 * (1 - u) + 0.003, 6, 6, goldFine));
  }
  // whiskers: long tapered curls from the nose pad
  for (const s of [-1, 1]) {
    const w0 = on(V(s * 0.45, 0.25, 1)).p;
    g.add(taperTube(new THREE.CatmullRomCurve3([w0, w0.clone().add(V(s * 0.16, 0.04, 0.02)), w0.clone().add(V(s * 0.3, -0.06, -0.12)), w0.clone().add(V(s * 0.32, -0.24, -0.24)), w0.clone().add(V(s * 0.24, -0.34, -0.2))]), (u) => 0.02 * (1 - u) + 0.004, 32, 6, goldFine));
    jaw.add(taperTube(new THREE.CatmullRomCurve3([V(s * 0.06, -0.1, 0.4), V(s * 0.08, -0.26, 0.36), V(s * 0.04, -0.38, 0.28)]), (u) => 0.028 * (1 - u) + 0.004, 12, 6, goldFine));
  }
  // mane: flame tufts fanned round the back of the skull, cheek frills
  for (let k = 0; k < 13; k++) {
    const a = -1.5 + (3.0 * k) / 12, m0 = on(V(Math.sin(a) * 0.8, Math.cos(a) * 0.8, -0.6));
    const t = tuft(goldFine, 0.42 + r() * 0.16, 0.25 + r() * 0.2); t.position.copy(m0.p); t.rotation.set(-0.7, a * 0.8, -a * 0.9); g.add(t);
  }
  for (const s of [-1, 1]) for (let k = 0; k < 4; k++) { const c0 = on(V(s, -0.1 - k * 0.15, -0.15 - k * 0.12)); const t = tuft(goldFine, 0.24, 0.12); t.position.copy(c0.p); t.rotation.set(0.4, s * 1.5, s * 0.5); g.add(t); }
  // the neck: an S-curve back and down into the wall it grows from, scaled, a spine of fins
  if (o.neck !== false) {
    const nc = new THREE.CatmullRomCurve3([V(0, 0.02, -0.18), V(0, -0.08, -0.5), V(0, -0.42, -0.66), V(0, -0.82, -0.58), V(0, -1.12, -0.72)]);
    g.add(taperTube(nc, (u) => 0.19 + 0.05 * Math.sin(u * Math.PI), 40, 16, scaleGold));
    for (let k = 1; k < 9; k++) { const u = k / 9, p = nc.getPointAt(u), tn = nc.getTangentAt(u); const fin = tuft(goldFine, 0.15, 0.05); fin.position.copy(p).add(V(0, 0, -0.17)); fin.lookAt(p.clone().add(V(0, 0, -1))); fin.rotateX(-Math.PI / 2 + Math.atan2(tn.y, -tn.z) * 0.5); g.add(fin); }
  }
  return shadowed(g) as THREE.Group;
}

/** a lathed vessel: profile [[radius, y]...], body material, relief bands at the given heights, an optional lid knob */
export function vessel(profile: [number, number][], o: { body?: THREE.Material; band?: THREE.Material; bands?: [number, number][]; knob?: number } = {}): THREE.Group {
  const g = new THREE.Group();
  const body = new THREE.Mesh(new THREE.LatheGeometry(profile.map(([r, y]) => new THREE.Vector2(r, y)), 72), o.body ?? metal("darkBronze", { relief: true, repeat: [8, 6] }));
  g.add(body);
  const band = o.band ?? metal("bronze", { relief: true, repeat: [10, 1] });
  for (const [y, r] of o.bands ?? []) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(r * 1.015, r * 1.015, 0.16, 72, 1, true), band); b.position.y = y; g.add(b);
    for (const dy of [-0.09, 0.09]) { const t = new THREE.Mesh(new THREE.TorusGeometry(r * 1.02, 0.022, 8, 72), metal("bronze")); t.rotation.x = Math.PI / 2; t.position.y = y + dy; g.add(t); }
  }
  if (o.knob) { const k = new THREE.Mesh(new THREE.SphereGeometry(o.knob, 20, 14), metal("bronze", { grain: true })); k.position.y = profile[profile.length - 1][1] + o.knob * 0.7; g.add(k); }
  return shadowed(g) as THREE.Group;
}

/** a squat toad (stone, bronze or glaze) with an open mouth gazing up, warty skin */
export function toad(o: { mat?: THREE.Material } = {}): THREE.Group {
  const g = new THREE.Group(), mat = o.mat ?? metal("darkBronze", { grain: true, rough: 0.6 });
  const body = new THREE.Mesh(sculpt((p) => { const w = 1 + 0.04 * Math.sin(p.x * 17) * Math.sin(p.z * 13) * Math.max(0, p.y); return V(p.x * 0.36 * w, (p.y > 0 ? p.y * 0.26 : p.y * 0.1) * w, p.z * 0.4 * w); }), mat);
  body.position.y = 0.12; g.add(body);
  const head = new THREE.Mesh(sculpt((p) => V(p.x * 0.27, p.y * (p.y > 0 ? 0.2 : 0.1), p.z * 0.24)), mat); head.position.set(0, 0.32, 0.2); head.rotation.x = -0.5; g.add(head);
  const lip = new THREE.Mesh(new THREE.TorusGeometry(0.13, 0.03, 10, 28), mat); lip.position.set(0, 0.42, 0.28); lip.rotation.x = -Math.PI / 2 + 0.6; g.add(lip);
  const hole = new THREE.Mesh(new THREE.CircleGeometry(0.12, 24), new THREE.MeshStandardMaterial({ color: "#140e10", roughness: 1 })); hole.position.set(0, 0.425, 0.285); hole.rotation.x = -Math.PI / 2 + 0.6; g.add(hole);
  for (const s of [-1, 1]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.075, 14, 10), mat); eye.position.set(s * 0.16, 0.45, 0.12); g.add(eye);
    const pup = new THREE.Mesh(new THREE.SphereGeometry(0.035, 10, 8), glaze("#1a1410", { rough: 0.15 })); pup.position.set(s * 0.18, 0.5, 0.16); g.add(pup);
    const leg = new THREE.Mesh(sculpt((p) => V(p.x * 0.09, p.y * 0.06, p.z * 0.2)), mat); leg.position.set(s * 0.3, 0.05, 0.22); leg.rotation.y = s * 0.5; g.add(leg);
    const haunch = new THREE.Mesh(sculpt((p) => V(p.x * 0.14, p.y * 0.12, p.z * 0.22)), mat); haunch.position.set(s * 0.3, 0.12, -0.1); g.add(haunch);
  }
  return shadowed(g) as THREE.Group;
}

/** a metal ball */
export function orb(kind: MetalKind = "bronze", r = 0.085): THREE.Mesh {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 24, 16), metal(kind, { grain: false, rough: 0.22 })); m.castShadow = true; return m;
}
