// The Vasa as a 3D model (our own modelling, simplified, about 1:1 in metres): a lofted oak hull with tumblehome and a
// high stern castle, two rows of gun ports with red lids and bronze muzzles, three masts with yards and four sails that
// can be set, a gilded stern and rails, a bow beak. The ship group's origin sits on the waterline amidships; x runs
// stern (-) to bow (+), port side is +z. heel > 0 rolls her to port (the side she went over on), sink lowers her.
import * as THREE from "three";
import { lambert } from "../kit/sets";
import { hullPlanks, sailTex, sternTex } from "./paint";

export const HULL_L = 47, HALF_B = 5.85, DRAFT = 4.8;
const X0 = -HULL_L / 2;
const clamp01 = (u: number) => Math.min(1, Math.max(0, u));

/** beam factor along the length (u: 0 stern .. 1 bow) */
const bfac = (u: number) => (u < 0.12 ? 0.62 + 0.38 * (u / 0.12) : u < 0.58 ? 1 : Math.pow(Math.max(0, Math.cos(((Math.min(u, 1) - 0.58) / 0.42) * Math.PI / 2)), 0.75));
/** deck (sheer) height above the waterline */
export const deckTop = (u: number) => 4.6 + (u < 0.26 ? 4.6 * Math.pow(1 - u / 0.26, 1.4) : 0) + (u > 0.82 ? 1.6 * Math.pow((u - 0.82) / 0.18, 2) : 0);
const draft = (u: number) => DRAFT * (u < 0.08 ? 0.75 + 0.25 * (u / 0.08) : u > 0.86 ? 1 - 0.65 * ((u - 0.86) / 0.14) : 1);
/** hull half-width at u and height y */
export function halfW(u: number, y: number) {
  const b = HALF_B * bfac(u);
  if (y < 0) return b * Math.max(0, 1 - Math.pow(-y / draft(u), 2.2));
  return b * (1 - 0.2 * Math.pow(y / deckTop(u), 1.6));
}
export const uOf = (x: number) => clamp01((x - X0) / HULL_L);
/** deck height at ship x */
export const deckY = (x: number) => deckTop(uOf(x)) - 0.25;

function hullGeometry(nu = 56, nv = 22) {
  const pos: number[] = [], uv: number[] = [], idx: number[] = [];
  // two sides: side = +1 (port, +z) and -1 (starboard)
  for (const side of [1, -1]) {
    const base = pos.length / 3;
    for (let i = 0; i <= nu; i++) {
      const u = i / nu, x = X0 + u * HULL_L, top = deckTop(u), dr = draft(u);
      for (let j = 0; j <= nv; j++) {
        const v = j / nv, y = -dr + v * (top + dr);
        const z = side * Math.max(0.02, halfW(u, y));
        pos.push(x, y, z); uv.push(x / 8, (y + DRAFT) / (10 + DRAFT));
      }
    }
    for (let i = 0; i < nu; i++) for (let j = 0; j < nv; j++) {
      const a = base + i * (nv + 1) + j, b = a + nv + 1;
      if (side > 0) idx.push(a, b, a + 1, b, b + 1, a + 1); else idx.push(a, a + 1, b, b, a + 1, b + 1);
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}
function deckGeometry(nu = 56) {
  const pos: number[] = [], uv: number[] = [], idx: number[] = [];
  for (let i = 0; i <= nu; i++) {
    const u = i / nu, x = X0 + u * HULL_L, y = deckTop(u) - 0.25, w = halfW(u, y) - 0.15;
    pos.push(x, y, w, x, y, -w); uv.push(x / 3, 0, x / 3, w / 3);
  }
  for (let i = 0; i < nu; i++) { const a = i * 2; idx.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
  g.setIndex(idx); g.computeVertexNormals();
  return g;
}

export type ShipState = { heel?: number; pitch?: number; sink?: number; sails?: number; lids?: number; guns?: number; masts?: boolean; yaw?: number; x?: number; z?: number };

export class Ship {
  readonly group = new THREE.Group();       // world placement (x, z, yaw, sink)
  readonly body = new THREE.Group();        // heel / pitch pivot at the waterline
  private lids: THREE.Object3D[] = [];
  private muzzles: THREE.Object3D[] = [];
  private sails: THREE.Mesh[] = [];
  private rig = new THREE.Group();
  /** gun port centres in ship space (side, row, x, y, z) */
  readonly ports: { side: number; row: number; p: THREE.Vector3 }[] = [];

  constructor(opts: { carvings?: boolean } = {}) {
    this.group.add(this.body);
    const oak = lambert({ map: hullPlanks([6, 1]), side: THREE.DoubleSide });
    const hull = new THREE.Mesh(hullGeometry(), oak); hull.castShadow = true; hull.receiveShadow = true; this.body.add(hull);
    const deckMat = lambert({ map: hullPlanks([1, 6], 7), side: THREE.DoubleSide });
    const deck = new THREE.Mesh(deckGeometry(), deckMat); deck.receiveShadow = true; this.body.add(deck);
    const red = lambert({ color: "#b8352a" }), gold = lambert({ color: "#e0aa36" }), dark = lambert({ color: "#1a1424" });
    const bronze = lambert({ color: "#9a6b2c" }), wood = lambert({ color: "#5b3a22" }), rope = lambert({ color: "#3a2a1c" });
    // gold rail along the sheer, both sides
    for (const side of [1, -1]) {
      const pts: THREE.Vector3[] = [];
      for (let i = 0; i <= 40; i++) { const u = i / 40, x = X0 + u * HULL_L, y = deckTop(u); pts.push(new THREE.Vector3(x, y + 0.05, side * (halfW(u, y) + 0.02))); }
      const rail = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 0.12, 6), gold); this.body.add(rail);
      // a painted red strake between the gun rows
      const strake: THREE.Vector3[] = [];
      for (let i = 2; i <= 36; i++) { const u = i / 40, x = X0 + u * HULL_L; strake.push(new THREE.Vector3(x, 2.6, side * (halfW(u, 2.6) + 0.03))); }
      this.body.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(strake), 60, 0.16, 4), red));
    }
    // gun ports: lower row y 1.45 (about 1.2 m sill above the water), upper row y 3.75; 12 a side per row
    const portGeo = new THREE.BoxGeometry(0.8, 0.8, 0.14), lidGeo = new THREE.BoxGeometry(0.86, 0.86, 0.08);
    const muzzleGeo = new THREE.CylinderGeometry(0.17, 0.2, 1.1, 12); muzzleGeo.rotateX(Math.PI / 2);
    for (const [row, y] of [[0, 1.45], [1, 3.75]] as [number, number][]) for (let k = 0; k < 12; k++) {
      const x = -16.5 + k * 2.75 + row * 0.6;
      const u = uOf(x);
      for (const side of [1, -1]) {
        const w = halfW(u, y);
        const port = new THREE.Mesh(portGeo, dark); port.position.set(x, y, side * (w + 0.0)); this.body.add(port);
        const hinge = new THREE.Group(); hinge.position.set(x, y + 0.43, side * (w + 0.08)); this.body.add(hinge);
        const lid = new THREE.Mesh(lidGeo, red); lid.position.set(0, -0.43, 0); lid.castShadow = true; hinge.add(lid);
        hinge.userData.side = side; this.lids.push(hinge);
        const m = new THREE.Mesh(muzzleGeo, bronze); m.position.set(x, y - 0.05, side * (w + 0.35)); m.visible = false; this.body.add(m); this.muzzles.push(m);
        this.ports.push({ side, row, p: new THREE.Vector3(x, y, side * w) });
      }
    }
    // stern: the gilded transom and the stern-castle galleries
    const sternU = 0.004, sy = deckTop(sternU), sw = halfW(sternU, sy * 0.6);
    if (opts.carvings !== false) {
      const panel = new THREE.Mesh(new THREE.PlaneGeometry(sw * 1.75, sy * 0.9), lambert({ map: sternTex() }));
      panel.position.set(X0 - 0.08, sy * 0.52, 0); panel.rotation.y = -Math.PI / 2; this.body.add(panel);
      // the carvings: rows of small gilded figures framing the transom and running along the stern quarters
      const fig = new THREE.CapsuleGeometry(0.16, 0.55, 4, 8), head = new THREE.SphereGeometry(0.17, 10, 8);
      const addFig = (x: number, y: number, z: number) => {
        const f = new THREE.Mesh(fig, gold); f.position.set(x, y, z); this.body.add(f);
        const h = new THREE.Mesh(head, gold); h.position.set(x, y + 0.48, z); this.body.add(h);
      };
      for (let i = 0; i < 9; i++) { const y = 1.2 + i * (sy * 0.85 / 9); addFig(X0 - 0.15, y, sw * 0.92); addFig(X0 - 0.15, y, -sw * 0.92); }
      for (let i = 0; i < 7; i++) addFig(X0 - 0.15, sy * 0.97 + 0.2, -sw * 0.75 + i * (sw * 1.5 / 6));
      for (const side of [1, -1]) for (let i = 0; i < 8; i++) {
        const x = X0 + 0.8 + i * 0.75, u = uOf(x), y = deckTop(u) - 1.2;
        addFig(x, y, side * (halfW(u, y) + 0.12));
      }
    }
    for (const side of [1, -1]) {
      const gal = new THREE.Mesh(new THREE.BoxGeometry(5, 1.3, 0.5), gold); gal.position.set(X0 + 3.2, sy - 2.4, side * (halfW(0.07, sy - 2.4) + 0.25)); this.body.add(gal);
    }
    // bow beak with a gold lion figurehead
    const beak = new THREE.Mesh(new THREE.ConeGeometry(0.9, 6, 4), wood); beak.rotation.z = -Math.PI / 2; beak.position.set(-X0 + 2.6, 3.4, 0); beak.castShadow = true; this.body.add(beak);
    const lionHead = new THREE.Mesh(new THREE.SphereGeometry(0.9, 14, 10), gold); lionHead.position.set(-X0 + 5.2, 4.1, 0); this.body.add(lionHead);
    // masts, yards, sails
    this.body.add(this.rig);
    const sail = lambert({ map: sailTex(), side: THREE.DoubleSide });
    const mast = (x: number, h: number, r: number) => {
      const y0 = deckY(x);
      const m = new THREE.Mesh(new THREE.CylinderGeometry(r * 0.55, r, h, 10), wood); m.position.set(x, y0 + h / 2, 0); m.castShadow = true; this.rig.add(m);
      return y0;
    };
    const yard = (x: number, y: number, len: number) => {
      const yd = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.2, len, 8), wood); yd.rotation.x = Math.PI / 2; yd.position.set(x, y, 0); yd.castShadow = true; this.rig.add(yd);
    };
    const addSail = (x: number, yTop: number, w: number, h: number) => {
      const g = new THREE.PlaneGeometry(w, h, 8, 6); g.translate(0, -h / 2, 0);
      const p = g.attributes.position as THREE.BufferAttribute;
      for (let i = 0; i < p.count; i++) { const zz = p.getX(i) / (w / 2), yy = -p.getY(i) / h; p.setZ(i, 0.9 * (1 - zz * zz) * Math.sin(yy * Math.PI * 0.95)); }
      g.computeVertexNormals();
      const m = new THREE.Mesh(g, sail); m.rotation.y = Math.PI / 2; m.position.set(x + 0.3, yTop, 0); m.castShadow = true; this.rig.add(m); this.sails.push(m);
    };
    const yF = mast(13, 38, 0.55), yM = mast(1.5, 46, 0.7), yZ = mast(-13, 28, 0.45);
    const bow = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.4, 16, 8), wood); bow.rotation.z = -(Math.PI / 2 - 0.45); bow.position.set(-X0 + 5.5, 8.2, 0); this.rig.add(bow);
    yard(13, yF + 16, 15); yard(13, yF + 29, 10); yard(1.5, yM + 18, 18); yard(1.5, yM + 33, 12); yard(-13, yZ + 14, 9);
    addSail(13, yF + 16, 14, 12); addSail(13, yF + 29, 9.5, 11); addSail(1.5, yM + 33, 11.5, 12); addSail(-13, yZ + 14, 8.5, 9);
    // shrouds (a few lines down to the rail)
    for (const [x, top, yb] of [[13, yF + 29, yF], [1.5, yM + 33, yM], [-13, yZ + 14, yZ]] as [number, number, number][])
      for (const side of [1, -1]) for (const dx of [-2.2, 0, 2.2]) {
        const a = new THREE.Vector3(x, top, 0), b = new THREE.Vector3(x + dx, yb + 0.3, side * (halfW(uOf(x + dx), yb) + 0.1));
        const l = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, a.distanceTo(b), 4), rope);
        l.position.copy(a).lerp(b, 0.5); l.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize()); this.rig.add(l);
      }
    // flags
    const flag = (x: number, y: number) => { const f = new THREE.Mesh(new THREE.PlaneGeometry(3, 1.8), lambert({ color: "#2a5fae", side: THREE.DoubleSide })); f.position.set(x - 1.5, y, 0); this.rig.add(f);
      const cross = new THREE.Mesh(new THREE.PlaneGeometry(3, 0.35), lambert({ color: "#f2c230", side: THREE.DoubleSide })); cross.position.set(x - 1.5, y, 0.01); this.rig.add(cross); };
    flag(13, yF + 38.5); flag(1.5, yM + 46.5); flag(-13, yZ + 28.5);
  }

  /** world position of a point in ship space (after heel/sink) */
  toWorld(v: THREE.Vector3, out = new THREE.Vector3()) { this.group.updateMatrixWorld(true); return out.copy(v).applyMatrix4(this.body.matrixWorld); }

  update(s: ShipState) {
    this.group.position.set(s.x ?? 0, -(s.sink ?? 0), s.z ?? 0);
    this.group.rotation.y = s.yaw ?? 0;
    this.body.rotation.set(s.heel ?? 0, 0, s.pitch ?? 0);
    const sails = s.sails ?? 0;
    this.sails.forEach((m, i) => { const k = clamp01(sails * 1.25 - i * 0.08); m.scale.set(1, Math.max(0.04, k), 1); m.visible = k > 0.02; });
    const lids = s.lids ?? 0, guns = s.guns ?? 0;
    this.lids.forEach((h) => { h.rotation.x = -h.userData.side * lids * 1.35; });
    this.muzzles.forEach((m) => { m.visible = guns > 0.02; m.scale.set(1, 1, Math.max(0.05, guns)); });
    this.rig.visible = s.masts !== false;
  }
}
