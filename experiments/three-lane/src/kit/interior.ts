// Interior architecture kit (our own code; visual track round 3, replication lesson 2: "interiors are flat, purple and
// empty"). Carved and lathed pieces for palaces, halls and temples, in warm painted stone, real gold and lacquer, plus
// candle practicals that feed the glows, the bloom and the bokeh discs (kit/depth.ts).
//   stoneMat(o)                    warm beige ashlar (painted), the default for every piece
//   column(h, o)                   a column: moulded base, fluted shaft, flared capital with an abacus
//   archway(w, h, o)               a pointed (or round) arch frame, extruded, with a keystone
//   arcade(root, o)                columns + arches down both sides of an aisle
//   roseWindow(r)                  stone tracery ring and spokes over a glowing stained-glass disc (NOINK, blooms)
//   banner(w, h, o)                a hanging cloth with a painted emblem, gold border and fringe, on a gold rod
//   throne(o)                      a carved throne: high pointed back with tracery, gold frame and finials, red cushion
//   carpet(w, l, o)                a runner with borders and a medallion repeat
//   candelabra(o)                  a gold stand with n candles: flames bloom, returns their positions
//   candleWall(root, ...)          a row of wall candles / sconces
// A candle-lit room wants the "candle" light preset (kit/presets.ts) and env "candle" (kit/materials.ts).
import * as THREE from "three";
import { lambert, basic } from "./sets";
import { stoneCourses } from "./dressing";
import { metal, glaze } from "./materials";
import { NOINK } from "../ink";
import { rng } from "../paint";
import type { V3 } from "./Stage";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const ctex = (c: HTMLCanvasElement, rep: [number, number] = [1, 1]) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); t.anisotropy = 4; return t; };
const shadowed = <T extends THREE.Object3D>(g: T) => { g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } }); return g; };

/** warm beige ashlar (the references' candle-lit stone): painted courses, light and dark blocks */
export function stoneMat(o: { rep?: [number, number]; light?: number; hue?: number; seed?: number } = {}) {
  return lambert({ map: stoneCourses(o.rep ?? [1, 1], { hue: o.hue ?? 36, light: o.light ?? 66, seed: o.seed ?? 11, moss: false }) });
}
const plain = (col: string) => lambert({ color: col });

export function column(h = 6, o: { r?: number; mat?: THREE.Material; gold?: boolean } = {}): THREE.Group {
  const g = new THREE.Group(), r = o.r ?? 0.42, m = o.mat ?? plain("#d6c3a4");
  const base = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [r * 1.5, 0], [r * 1.5, 0.22], [r * 1.3, 0.3], [r * 1.35, 0.38], [r * 1.1, 0.48], [r, 0.55], [0, 0.55]].map(([x, y]) => new THREE.Vector2(x, y)), 32), m);
  g.add(base);
  // fluted shaft: radius modulated round the circumference
  const shaft = new THREE.CylinderGeometry(r * 0.92, r, h - 1.3, 48, 6, true), p = shaft.getAttribute("position") as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), z = p.getZ(i), a = Math.atan2(z, x), k = 1 - 0.05 * Math.max(0, Math.cos(a * 16)); p.setX(i, x * k); p.setZ(i, z * k); }
  shaft.computeVertexNormals();
  const sh = new THREE.Mesh(shaft, m); sh.position.y = 0.55 + (h - 1.3) / 2; g.add(sh);
  const cap = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [r * 0.95, 0], [r * 1.05, 0.08], [r * 1.2, 0.3], [r * 1.55, 0.55], [r * 1.65, 0.6], [0, 0.6]].map(([x, y]) => new THREE.Vector2(x, y)), 32), o.gold ? metal("gold", { grain: true }) : m);
  cap.position.y = h - 0.75; g.add(cap);
  const abacus = new THREE.Mesh(new THREE.BoxGeometry(r * 3.6, 0.18, r * 3.6), m); abacus.position.y = h - 0.06; g.add(abacus);
  return shadowed(g);
}

/** a pointed (Gothic) or round arch frame in the x-y plane, `depth` thick, inner opening w x h (spring at h - w/2) */
export function archway(w = 3.2, h = 6, o: { depth?: number; band?: number; pointed?: boolean; mat?: THREE.Material } = {}): THREE.Group {
  const g = new THREE.Group(), b = o.band ?? 0.45, d = o.depth ?? 0.6, m = o.mat ?? plain("#cdb795");
  const outline = (W: number, H: number) => {
    const s = new THREE.Shape(), hw = W / 2, spring = H - (o.pointed === false ? hw : hw * 1.2);
    s.moveTo(-hw, 0); s.lineTo(-hw, spring);
    if (o.pointed === false) s.absarc(0, spring, hw, Math.PI, 0, true);
    else { s.quadraticCurveTo(-hw, H - hw * 0.15, 0, H); s.quadraticCurveTo(hw, H - hw * 0.15, hw, spring); }
    s.lineTo(hw, 0); s.lineTo(-hw, 0); return s;
  };
  const outer = outline(w + 2 * b, h + b), inner = outline(w, h);
  const ring = new THREE.Shape(outer.getPoints(48)); ring.holes.push(new THREE.Path(inner.getPoints(48)));
  const geo = new THREE.ExtrudeGeometry(ring, { depth: d, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 2, curveSegments: 24 });
  geo.translate(0, 0, -d / 2);
  g.add(new THREE.Mesh(geo, m));
  const key = new THREE.Mesh(new THREE.BoxGeometry(b * 0.9, b * 1.2, d * 1.1), m); key.position.set(0, h + b * 0.3, 0); g.add(key);
  return shadowed(g);
}

/** columns and arches down both sides of an aisle running along z */
export function arcade(root: THREE.Object3D, o: { x: number; z0: number; z1: number; step?: number; h?: number; mat?: THREE.Material; gold?: boolean }) {
  const step = o.step ?? 3.6, h = o.h ?? 6.5;
  for (let z = o.z0; z > o.z1; z -= step) for (const s of [-1, 1]) {
    const c = column(h, { mat: o.mat, gold: o.gold }); c.position.set(s * o.x, 0, z); root.add(c);
    if (z - step > o.z1) { const a = archway(step - 1.1, 2.2, { depth: 0.7, mat: o.mat }); a.position.set(s * o.x, h, z - step / 2); a.rotation.y = Math.PI / 2; root.add(a); }
  }
}

function glassTex(seed = 5) {
  const [c, g] = canvas(512, 512), r = rng(seed), cols = ["#e0a43c", "#c0392b", "#2f6fb5", "#7a4bb0", "#2f9a6a", "#f2d27a"];
  g.fillStyle = "#3a2a3a"; g.fillRect(0, 0, 512, 512);
  for (let ring = 0; ring < 3; ring++) {
    const r0 = 60 + ring * 62, r1 = r0 + 58, n = 8 + ring * 8;
    for (let k = 0; k < n; k++) {
      const a0 = (k / n) * Math.PI * 2, a1 = ((k + 1) / n) * Math.PI * 2;
      g.fillStyle = cols[Math.floor(r() * cols.length)];
      g.beginPath(); g.arc(256, 256, r1, a0 + 0.03, a1 - 0.03); g.arc(256, 256, r0, a1 - 0.03, a0 + 0.03, true); g.closePath(); g.fill();
      g.fillStyle = "rgba(255,255,255,0.18)"; g.beginPath(); g.arc(256 + Math.cos((a0 + a1) / 2) * (r0 + 14), 256 + Math.sin((a0 + a1) / 2) * (r0 + 14), 7, 0, 7); g.fill();
    }
  }
  const grd = g.createRadialGradient(256, 256, 0, 256, 256, 60); grd.addColorStop(0, "#fff2c0"); grd.addColorStop(1, "#e0a43c");
  g.fillStyle = grd; g.beginPath(); g.arc(256, 256, 58, 0, 7); g.fill();
  return ctex(c);
}
/** a rose window: glowing glass (NOINK, blooms) behind a stone tracery ring with spokes and foils */
export function roseWindow(R = 1.9, o: { mat?: THREE.Material; glow?: number } = {}): THREE.Group {
  const g = new THREE.Group(), m = o.mat ?? plain("#cdb795");
  const glass = new THREE.Mesh(new THREE.CircleGeometry(R, 64), basic({ map: glassTex() }));
  (glass.material as THREE.MeshBasicMaterial).color.setScalar(o.glow ?? 1.35); glass.layers.set(NOINK); glass.userData.bloom = true; g.add(glass);
  const tr = (rad: number, t: number) => { const ring = new THREE.Mesh(new THREE.TorusGeometry(rad, t, 10, 64), m); ring.position.z = 0.06; g.add(ring); };
  tr(R, 0.16); tr(R * 0.38, 0.07); tr(R * 0.68, 0.05);
  for (let k = 0; k < 16; k++) { const a = (k / 16) * Math.PI * 2, sp = new THREE.Mesh(new THREE.BoxGeometry(0.06, R * 0.62, 0.08), m); sp.position.set(Math.cos(a) * R * 0.69, Math.sin(a) * R * 0.69, 0.06); sp.rotation.z = a - Math.PI / 2; g.add(sp); }
  for (let k = 0; k < 8; k++) { const a = ((k + 0.5) / 8) * Math.PI * 2, foil = new THREE.Mesh(new THREE.TorusGeometry(R * 0.13, 0.03, 8, 24), m); foil.position.set(Math.cos(a) * R * 0.86, Math.sin(a) * R * 0.86, 0.06); g.add(foil); }
  return shadowed(g);
}

function bannerTex(col: string, emblem: string, seed = 3) {
  const [c, g] = canvas(256, 512), r = rng(seed);
  g.fillStyle = col; g.fillRect(0, 0, 256, 512);
  for (let k = 0; k < 40; k++) { g.fillStyle = `rgba(0,0,0,${0.03 + r() * 0.04})`; g.fillRect(r() * 256, 0, 3 + r() * 10, 512); }       // folds
  g.strokeStyle = "#e0b045"; g.lineWidth = 14; g.strokeRect(14, 14, 228, 440);
  g.lineWidth = 4; g.strokeRect(30, 30, 196, 408);
  g.fillStyle = emblem; g.beginPath(); g.arc(128, 220, 62, 0, 7); g.fill();
  g.strokeStyle = "#e0b045"; g.lineWidth = 6; g.beginPath(); g.arc(128, 220, 62, 0, 7); g.stroke();
  g.fillStyle = col; g.beginPath(); for (let k = 0; k < 10; k++) { const a = (k / 10) * Math.PI * 2 - Math.PI / 2, rr = k % 2 ? 22 : 48; g.lineTo(128 + Math.cos(a) * rr, 220 + Math.sin(a) * rr); } g.closePath(); g.fill();
  g.fillStyle = "#e0b045"; for (let x = 8; x < 256; x += 16) { g.beginPath(); g.moveTo(x, 470); g.lineTo(x + 8, 470); g.lineTo(x + 4, 512); g.fill(); }
  return ctex(c);
}
/** a hanging banner (faces +z): painted emblem, gold border and fringe, a gold rod with finials, a soft curl */
export function banner(w = 1.2, h = 3.2, o: { color?: string; emblem?: string; seed?: number } = {}): THREE.Group {
  const g = new THREE.Group();
  const geo = new THREE.PlaneGeometry(w, h, 8, 12), p = geo.getAttribute("position") as THREE.BufferAttribute;
  for (let i = 0; i < p.count; i++) p.setZ(i, 0.05 * Math.sin((p.getX(i) / w) * Math.PI * 3) * (0.5 - p.getY(i) / h));
  geo.computeVertexNormals();
  const cloth = new THREE.Mesh(geo, lambert({ map: bannerTex(o.color ?? "#9a2230", o.emblem ?? "#2a1a40", o.seed), side: THREE.DoubleSide })); cloth.position.y = -h / 2; g.add(cloth);
  const gold = metal("gold", { grain: true });
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, w + 0.4, 10), gold); rod.rotation.z = Math.PI / 2; g.add(rod);
  for (const s of [-1, 1]) { const f = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), gold); f.position.x = s * (w / 2 + 0.2); g.add(f); }
  return shadowed(g);
}

function tuftTex(base = "#a8262c") {
  const [c, g] = canvas(256, 256);
  g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  for (let y = 16; y < 256; y += 32) for (let x = (y / 32) % 2 ? 32 : 16; x < 256; x += 32) {
    const grd = g.createRadialGradient(x, y, 0, x, y, 16); grd.addColorStop(0, "rgba(0,0,0,0.35)"); grd.addColorStop(1, "rgba(0,0,0,0)"); g.fillStyle = grd; g.fillRect(x - 16, y - 16, 32, 32);
    g.fillStyle = "#e3a640"; g.beginPath(); g.arc(x, y, 3.5, 0, 7); g.fill();
  }
  return ctex(c, [2, 3]);
}
/** a carved throne facing +z: seat, high pointed back with a tracery panel, gold frame, finials and a crest */
export function throne(o: { cushion?: string; wood?: THREE.Material } = {}): THREE.Group {
  const g = new THREE.Group(), gold = metal("gold", { grain: true }), wood = o.wood ?? glaze("#5a1e1a", { rough: 0.45 });
  const back = new THREE.Shape(); back.moveTo(-0.8, 0); back.lineTo(-0.8, 2.3); back.quadraticCurveTo(-0.8, 3.1, 0, 3.5); back.quadraticCurveTo(0.8, 3.1, 0.8, 2.3); back.lineTo(0.8, 0); back.lineTo(-0.8, 0);
  const bk = new THREE.Mesh(new THREE.ExtrudeGeometry(back, { depth: 0.18, bevelEnabled: true, bevelSize: 0.05, bevelThickness: 0.05, bevelSegments: 2 }), wood); bk.position.set(0, 0.6, -0.3); g.add(bk);
  const panel = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 2.0), lambert({ map: tuftTex(o.cushion ?? "#a8262c") })); panel.position.set(0, 1.85, -0.06); g.add(panel);
  const rim = new THREE.Shape(); rim.moveTo(-0.66, 0); rim.lineTo(-0.66, 2.0); rim.quadraticCurveTo(-0.66, 2.6, 0, 2.9); rim.quadraticCurveTo(0.66, 2.6, 0.66, 2.0); rim.lineTo(0.66, 0);
  const rimTube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(rim.getPoints(40).map((p) => new THREE.Vector3(p.x, p.y, 0))), 80, 0.045, 8), gold); rimTube.position.set(0, 0.75, -0.05); g.add(rimTube);
  const seat = new THREE.Mesh(new THREE.BoxGeometry(1.7, 0.55, 1.0), wood); seat.position.set(0, 0.32, 0.25); g.add(seat);
  const cush = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.14, 0.85), lambert({ color: o.cushion ?? "#b8302f" })); cush.position.set(0, 0.66, 0.27); g.add(cush);
  const band = new THREE.Mesh(new THREE.BoxGeometry(1.74, 0.1, 1.04), gold); band.position.set(0, 0.56, 0.25); g.add(band);
  for (const s of [-1, 1]) {
    const arm = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.55, 0.95), wood); arm.position.set(s * 0.86, 0.85, 0.25); g.add(arm);
    const armCap = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 1.0, 12), gold); armCap.rotation.x = Math.PI / 2; armCap.position.set(s * 0.86, 1.14, 0.25); g.add(armCap);
    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.08, 3.2, 12), gold); post.position.set(s * 0.86, 1.6, -0.2); g.add(post);
    const fin = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.12, 0.05], [0.14, 0.18], [0.06, 0.3], [0.1, 0.38], [0, 0.6]].map(([x, y]) => new THREE.Vector2(x, y)), 16), gold); fin.position.set(s * 0.86, 3.2, -0.2); g.add(fin);
  }
  const crest = new THREE.Mesh(new THREE.TorusGeometry(0.22, 0.05, 10, 28), gold); crest.position.set(0, 4.15, -0.2); g.add(crest);
  const gem = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), glaze("#c0202a", { rough: 0.1 })); gem.position.set(0, 4.15, -0.17); g.add(gem);
  return shadowed(g);
}

function runnerTex(field: string, border: string, accent: string) {
  const [c, g] = canvas(256, 512);
  g.fillStyle = field; g.fillRect(0, 0, 256, 512);
  g.fillStyle = border; g.fillRect(0, 0, 28, 512); g.fillRect(228, 0, 28, 512);
  g.fillStyle = accent; g.fillRect(30, 0, 5, 512); g.fillRect(221, 0, 5, 512);
  for (let y = 0; y < 512; y += 24) { g.fillStyle = accent; g.fillRect(10, y + 8, 8, 8); g.fillRect(238, y + 8, 8, 8); }
  for (let y = 0; y < 512; y += 128) {
    g.strokeStyle = accent; g.lineWidth = 5; g.beginPath(); g.ellipse(128, y + 64, 62, 50, 0, 0, 7); g.stroke();
    g.fillStyle = border; g.beginPath(); g.moveTo(128, y + 26); g.lineTo(176, y + 64); g.lineTo(128, y + 102); g.lineTo(80, y + 64); g.closePath(); g.fill();
    g.fillStyle = accent; g.beginPath(); g.arc(128, y + 64, 9, 0, 7); g.fill();
  }
  return ctex(c);
}
/** a carpet runner along z (w x l), lying on y = 0 */
export function carpet(w = 2.6, l = 16, o: { field?: string; border?: string; accent?: string } = {}): THREE.Mesh {
  const t = runnerTex(o.field ?? "#8e1f26", o.border ?? "#5a1420", o.accent ?? "#e0a840"); t.repeat.set(1, Math.max(1, Math.round(l / w / 2)));
  const m = new THREE.Mesh(new THREE.BoxGeometry(w, 0.025, l), lambert({ map: t })); m.position.y = 0.0125; m.receiveShadow = true; return m;
}

/** a gold candelabra: a stem and `n` candles on curved arms; returns the flame positions (local) for bokeh / glows */
export function candelabra(o: { n?: number; h?: number; spread?: number } = {}): THREE.Group & { flames: V3[] } {
  const g = new THREE.Group() as THREE.Group & { flames: V3[] }, gold = metal("gold", { grain: true }), n = o.n ?? 5, h = o.h ?? 2.1, sp = o.spread ?? 0.45;
  const stem = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.3, 0], [0.32, 0.06], [0.1, 0.2], [0.05, 0.5], [0.08, 0.56], [0.045, 0.6], [0.04, h], [0, h]].map(([x, y]) => new THREE.Vector2(x, y)), 16), gold);
  g.add(stem);
  const wax = glaze("#f4ecd6", { rough: 0.6 }), flameMat = basic({ color: "#ffd890" }); flameMat.color.multiplyScalar(2.2);
  g.flames = [];
  for (let k = 0; k < n; k++) {
    const u = n === 1 ? 0 : (k / (n - 1)) * 2 - 1, x = u * sp, y = h + (k === Math.floor(n / 2) ? 0.18 : 0.02);
    if (x !== 0) { const arm = new THREE.Mesh(new THREE.TubeGeometry(new THREE.QuadraticBezierCurve3(new THREE.Vector3(0, h - 0.25, 0), new THREE.Vector3(x, h - 0.3, 0), new THREE.Vector3(x, y, 0)), 12, 0.022, 6), gold); g.add(arm); }
    const cup = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.035, 0.05, 12), gold); cup.position.set(x, y, 0); g.add(cup);
    const cd = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.22, 10), wax); cd.position.set(x, y + 0.13, 0); g.add(cd);
    const fl = new THREE.Mesh(new THREE.SphereGeometry(0.03, 8, 6), flameMat); fl.scale.set(1, 1.8, 1); fl.position.set(x, y + 0.3, 0); fl.layers.set(NOINK); fl.userData.bloom = true; g.add(fl);
    g.flames.push([x, y + 0.3, 0]);
  }
  return shadowed(g);
}
