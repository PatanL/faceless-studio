// Set detail and prop dressing (our own code). The coordinator's v14 note and the measurement in docs/RND_LOG.md
// ("src/next parity pieces", detail density): our sets read flat - bare colour, empty water and sky - where the
// references have painted wood grain, plank gaps, stone, rope, dense props and soft lit gradients. On frames30
// sheets (240p, caption band masked) Vasa v14 has flat-block share 0.48 against the refs' median 0.40 and edge density
// 0.073 against 0.092. These pieces close that gap and are plain functions any set can call:
//   textures   grainPlanks, stoneCourses, richWater (painted, seeded, with a soft top-lit gradient and edge shading)
//   props      crate, barrel, ropeCoil, sack, bucket, net, bollard, lanternPost (inked by the world pass; textured)
//   dress()    scatters a prop kit over an area, deterministic, keeping out of given boxes (where actors stand)
//   clouds()   inked painted cloud cards that fill an empty sky (NOINK, face the camera)
import * as THREE from "three";
import { NOINK } from "../ink";
import { rng } from "../paint";
import { lambert, glowSprite } from "../kit/sets";
import type { Box } from "../kit/framing";

/** A/B switch for measurement (DressLab): when bare, the painters return one flat colour and dress / clouds add
 * nothing - the look our sets had before these pieces */
let BARE = false;
export const setBare = (b: boolean) => { BARE = b; };
const flat = (col: string, repeat: [number, number]) => { const [c, g] = canvas(8, 8); g.fillStyle = col; g.fillRect(0, 0, 8, 8); return tex(c, repeat); };
const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const tex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => {
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); t.anisotropy = 8; return t;
};
const hsl = (h: number, s: number, l: number, a = 1) => `hsla(${h.toFixed(1)}, ${s.toFixed(1)}%, ${l.toFixed(1)}%, ${a})`;
/** a soft top-lit gradient over the whole canvas (lit surfaces in the refs are never one flat value) */
function litGradient(g: CanvasRenderingContext2D, w: number, h: number, k = 0.16) {
  const grd = g.createLinearGradient(0, 0, 0, h);
  grd.addColorStop(0, `rgba(255, 240, 210, ${k})`); grd.addColorStop(0.55, "rgba(0,0,0,0)"); grd.addColorStop(1, `rgba(30, 20, 60, ${k})`);
  g.fillStyle = grd; g.fillRect(0, 0, w, h);
}

// ------------------------------------------------------------------------------------------------ textures
/** planks with grain, knots, dark gaps, nail heads and per-board tone (decks, floors, crates, walls) */
export function grainPlanks(repeat: [number, number] = [1, 1], o: { hue?: number; light?: number; boards?: number; seed?: number; vertical?: boolean } = {}) {
  if (BARE) return flat(hsl(o.hue ?? 28, 40, o.light ?? 44), repeat);
  const S = 512, [c, g] = canvas(S, S), r = rng(o.seed ?? 3), n = o.boards ?? 6, hue = o.hue ?? 28, L = o.light ?? 44;
  const bw = S / n;
  for (let i = 0; i < n; i++) {
    const y0 = i * bw;
    g.fillStyle = hsl(hue + (r() - 0.5) * 8, 38 + r() * 14, L + (r() - 0.5) * 10); g.fillRect(0, y0, S, bw);
    for (let k = 0; k < 18; k++) {                                           // grain
      g.strokeStyle = `rgba(55, 28, 10, ${0.06 + r() * 0.12})`; g.lineWidth = 1 + r() * 2.5;
      const yy = y0 + 4 + r() * (bw - 8); g.beginPath(); g.moveTo(0, yy);
      for (let x = 0; x <= S; x += 32) g.lineTo(x, yy + Math.sin(x * 0.02 + k) * 2 + (r() - 0.5) * 2);
      g.stroke();
    }
    for (let k = 0; k < 2; k++) if (r() < 0.6) {                             // knots
      const x = r() * S, y = y0 + bw * (0.3 + r() * 0.4);
      g.fillStyle = "rgba(60, 30, 12, 0.55)"; g.beginPath(); g.ellipse(x, y, 10 + r() * 8, 5 + r() * 3, 0, 0, Math.PI * 2); g.fill();
      g.strokeStyle = "rgba(60, 30, 12, 0.35)"; g.lineWidth = 2; g.beginPath(); g.ellipse(x, y, 20, 9, 0, 0, Math.PI * 2); g.stroke();
    }
    const butt = r() * S;                                                     // a butt joint and its nails
    g.fillStyle = "rgba(25, 12, 6, 0.85)"; g.fillRect(butt, y0, 4, bw);
    g.fillStyle = "rgba(40, 30, 30, 0.9)";
    for (const dy of [0.25, 0.75]) { g.beginPath(); g.arc(butt - 9, y0 + bw * dy, 3, 0, 7); g.arc(butt + 13, y0 + bw * dy, 3, 0, 7); g.fill(); }
    g.fillStyle = "rgba(20, 10, 5, 0.9)"; g.fillRect(0, y0, S, 5);          // the gap
    g.fillStyle = "rgba(255, 230, 190, 0.12)"; g.fillRect(0, y0 + 5, S, 3);  // the lit edge under it
  }
  litGradient(g, S, S, 0.12);
  const t = tex(c, repeat);
  if (o.vertical) t.rotation = Math.PI / 2;
  return t;
}
/** stone courses: blocks with mortar, chipped corners, a lit top edge and a little moss */
export function stoneCourses(repeat: [number, number] = [1, 1], o: { hue?: number; light?: number; seed?: number; moss?: boolean } = {}) {
  if (BARE) return flat(hsl(o.hue ?? 32, 12, o.light ?? 58), repeat);
  const S = 512, [c, g] = canvas(S, S), r = rng(o.seed ?? 7), hue = o.hue ?? 32, L = o.light ?? 58;
  g.fillStyle = hsl(hue, 10, L - 24); g.fillRect(0, 0, S, S);
  const rowH = 64;
  for (let y = 0, k = 0; y < S; y += rowH, k++) {
    let x = k % 2 ? -50 : 0;
    while (x < S) {
      const w = 90 + r() * 70, l = L + (r() - 0.5) * 12;
      g.fillStyle = hsl(hue + (r() - 0.5) * 14, 10 + r() * 10, l);
      g.beginPath(); g.roundRect(x + 4, y + 4, w - 8, rowH - 8, 8); g.fill();
      g.fillStyle = `hsla(${hue}, 20%, ${l + 14}%, 0.6)`; g.fillRect(x + 8, y + 6, w - 16, 4);         // lit top edge
      g.fillStyle = `hsla(${hue}, 20%, ${l - 16}%, 0.5)`; g.fillRect(x + 8, y + rowH - 12, w - 16, 5); // shaded bottom
      for (let q = 0; q < 5; q++) { g.fillStyle = `rgba(40, 30, 40, ${0.08 + r() * 0.1})`; g.beginPath(); g.arc(x + r() * w, y + r() * rowH, 2 + r() * 5, 0, 7); g.fill(); }
      if (o.moss !== false && r() < 0.18) { g.fillStyle = "rgba(90, 130, 60, 0.55)"; g.beginPath(); g.ellipse(x + r() * w, y + rowH - 10, 18, 6, 0, 0, 7); g.fill(); }
      x += w;
    }
  }
  litGradient(g, S, S, 0.14);
  return tex(c, repeat);
}
/** water with painted wave strokes, foam flecks, darker troughs and light streaks (fills empty water) */
export function richWater(repeat: [number, number] = [30, 30], o: { deep?: boolean; seed?: number } = {}) {
  if (BARE) return flat(o.deep ? "#1f4f6e" : "#3d8aa2", repeat);
  const S = 512, [c, g] = canvas(S, S), r = rng(o.seed ?? 5);
  g.fillStyle = o.deep ? "#1f4f6e" : "#3d8aa2"; g.fillRect(0, 0, S, S);
  for (let i = 0; i < 40; i++) { g.fillStyle = o.deep ? "rgba(10, 40, 60, 0.3)" : "rgba(25, 85, 115, 0.32)"; g.beginPath(); g.ellipse(r() * S, r() * S, 30 + r() * 60, 6 + r() * 10, 0, 0, 7); g.fill(); }
  for (let i = 0; i < 70; i++) {
    const x = r() * S, y = r() * S, w = 20 + r() * 70;
    g.strokeStyle = o.deep ? "rgba(150, 205, 225, 0.4)" : "rgba(225, 248, 252, 0.6)"; g.lineWidth = 2 + r() * 3; g.lineCap = "round";
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 7, x + w, y); g.stroke();
  }
  for (let i = 0; i < 120; i++) { g.fillStyle = "rgba(240, 252, 255, 0.55)"; g.fillRect(r() * S, r() * S, 2 + r() * 3, 1.5); }
  return tex(c, repeat);
}

// ------------------------------------------------------------------------------------------------ props
let plankMat: THREE.Material | null = null, darkMat: THREE.Material | null = null;
const planksM = () => (plankMat ??= lambert({ map: grainPlanks([1, 1], { hue: 30, light: 50, boards: 4, seed: 11 }) }));
const ironM = () => (darkMat ??= lambert({ color: "#3a3446" }));
export function crate(s = 0.6) {
  const g = new THREE.Group();
  const b = new THREE.Mesh(new THREE.BoxGeometry(s, s, s), planksM()); b.position.y = s / 2; b.castShadow = b.receiveShadow = true; g.add(b);
  const slat = lambert({ color: "#6b4426" });
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(s * 0.1, s * 1.02, s * 0.1), slat); p.position.set(sx * s * 0.46, s / 2, sz * s * 0.46); g.add(p); }
  const d = new THREE.Mesh(new THREE.BoxGeometry(s * 1.36, s * 0.08, s * 0.04), slat); d.rotation.z = Math.PI / 4; d.position.set(0, s / 2, s * 0.51); g.add(d);
  return g;
}
export function barrel(h = 0.8) {
  const g = new THREE.Group(), r = h * 0.36;
  const prof = [[0, 0], [r * 0.82, 0], [r, h * 0.5], [r * 0.82, h], [0, h]].map(([x, y]) => new THREE.Vector2(x, y));
  const m = new THREE.Mesh(new THREE.LatheGeometry(prof, 20), lambert({ map: grainPlanks([4, 1], { hue: 26, light: 40, boards: 3, seed: 21, vertical: true }) }));
  m.castShadow = m.receiveShadow = true; g.add(m);
  for (const y of [0.15, 0.5, 0.85]) { const k = 1 - Math.abs(y - 0.5) * 0.36; const hoop = new THREE.Mesh(new THREE.TorusGeometry(r * k * 1.01, h * 0.025, 6, 24), ironM()); hoop.rotation.x = Math.PI / 2; hoop.position.y = h * y; g.add(hoop); }
  return g;
}
export function ropeCoil(r = 0.3, turns = 4) {
  const g = new THREE.Group(), m = lambert({ color: "#b99460" });
  for (let i = 0; i < turns; i++) { const t = new THREE.Mesh(new THREE.TorusGeometry(r * (1 - i * 0.12), r * 0.09, 8, 28), m); t.rotation.x = Math.PI / 2; t.position.y = r * 0.09 * (1 + i * 1.6); t.castShadow = true; g.add(t); }
  return g;
}
export function sack(s = 0.5) {
  const g = new THREE.Group();
  const m = new THREE.Mesh(new THREE.SphereGeometry(s * 0.5, 14, 10), lambert({ color: "#c8ab78" })); m.scale.set(1, 1.15, 0.85); m.position.y = s * 0.52; m.castShadow = true; g.add(m);
  const tie = new THREE.Mesh(new THREE.CylinderGeometry(s * 0.1, s * 0.16, s * 0.2, 8), lambert({ color: "#a88a58" })); tie.position.y = s * 1.1; g.add(tie);
  return g;
}
export function bucket(s = 0.35) {
  const g = new THREE.Group();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(s * 0.5, s * 0.4, s, 16, 1, true), lambert({ color: "#8a6a4a", side: THREE.DoubleSide })); m.position.y = s / 2; m.castShadow = true; g.add(m);
  const water = new THREE.Mesh(new THREE.CircleGeometry(s * 0.46, 16), lambert({ color: "#3d7a96" })); water.rotation.x = -Math.PI / 2; water.position.y = s * 0.8; g.add(water);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(s * 0.5, s * 0.03, 6, 16, Math.PI), ironM()); handle.position.y = s; g.add(handle);
  return g;
}
export function net(w = 1.4, h = 1.0) {
  const [c, g] = canvas(256, 256);
  g.strokeStyle = "#e6d6b0"; g.lineWidth = 5;
  for (let k = 0; k <= 256; k += 32) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k, 256); g.stroke(); g.beginPath(); g.moveTo(0, k); g.lineTo(256, k); g.stroke(); }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), lambert({ map: tex(c, [3, 2]), alphaTest: 0.5, side: THREE.DoubleSide }));
  m.position.y = h / 2; m.castShadow = true;
  const gr = new THREE.Group(); gr.add(m); return gr;
}
export function bollard(h = 0.6) {
  const g = new THREE.Group();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(h * 0.22, h * 0.26, h, 12), ironM()); m.position.y = h / 2; m.castShadow = true; g.add(m);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(h * 0.3, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), ironM()); cap.position.y = h; g.add(cap);
  return g;
}
export function lanternPost(h = 2.2) {
  const g = new THREE.Group();
  const p = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.07, h, 8), ironM()); p.position.y = h / 2; p.castShadow = true; g.add(p);
  const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.3, 0.22), lambert({ color: "#f2d48a" })); lamp.position.y = h + 0.1; g.add(lamp);
  glowSprite(g, [255, 200, 120], 1.4, 0, h + 0.1, 0);
  return g;
}
export const PROPS = { crate, barrel, ropeCoil, sack, bucket, net, bollard, lanternPost } as const;
export type PropKind = keyof typeof PROPS;

/** scatter `n` props from `kit` over the area [x0, z0, x1, z1] at floor height y, deterministic. Props keep out of
 * `keep` boxes (actor spots, camera paths) and of each other; crates sometimes stack, sacks lean on things. Returns the
 * placed footprint boxes (for the caption / framing checks). */
export function dress(root: THREE.Object3D, o: { area: [number, number, number, number]; y?: number; n?: number; kit?: PropKind[]; keep?: Box[]; seed?: number; scale?: number }): Box[] {
  if (BARE) return [];
  const r = rng(o.seed ?? 9), kit = o.kit ?? ["crate", "barrel", "ropeCoil", "sack", "bucket"], y = o.y ?? 0, sc = o.scale ?? 1;
  const placed: Box[] = [];
  const [x0, z0, x1, z1] = o.area;
  const free = (b: Box) => ![...(o.keep ?? []), ...placed].some((k) => b[0] < k[3] && b[3] > k[0] && b[2] < k[5] && b[5] > k[2]);
  for (let i = 0, tries = 0; i < (o.n ?? 12) && tries < 400; tries++) {
    const kind = kit[Math.floor(r() * kit.length)], x = x0 + r() * (x1 - x0), z = z0 + r() * (z1 - z0), s = (0.8 + r() * 0.5) * sc;
    const half = (kind === "net" ? 0.7 : kind === "barrel" || kind === "crate" ? 0.38 : 0.3) * s;
    const b: Box = [x - half, y, z - half, x + half, y + 1.2 * s, z + half];
    if (!free(b)) continue;
    const m = (PROPS[kind] as (s: number) => THREE.Group)(kind === "crate" ? 0.6 * s : kind === "barrel" ? 0.8 * s : kind === "net" ? 1.4 * s : 0.4 * s);
    m.position.set(x, y, z); m.rotation.y = r() * Math.PI * 2; root.add(m);
    if (kind === "crate" && r() < 0.35) { const top = crate(0.45 * s); top.position.set(x + (r() - 0.5) * 0.1, y + 0.6 * s, z); top.rotation.y = r(); root.add(top); }
    placed.push(b); i++;
  }
  return placed;
}

// ------------------------------------------------------------------------------------------------ clouds
let cloudTex: THREE.Texture[] | null = null;
function cloudTextures() {
  if (cloudTex) return cloudTex;
  cloudTex = [0, 1, 2].map((k) => {
    const [c, g] = canvas(512, 256), r = rng(31 + k);
    const blobs = Array.from({ length: 7 }, (_, i) => [90 + i * 55 + (r() - 0.5) * 30, 150 - Math.sin((i / 6) * Math.PI) * 50 - r() * 20, 50 + r() * 40] as const);
    g.fillStyle = "#1b1240"; for (const [x, y, rr] of blobs) { g.beginPath(); g.arc(x, y, rr + 6, 0, 7); g.fill(); }
    g.fillRect(84, 150, 344, 56);
    g.fillStyle = "#f6f1ea"; for (const [x, y, rr] of blobs) { g.beginPath(); g.arc(x, y, rr, 0, 7); g.fill(); }
    g.fillRect(90, 150, 332, 50);
    g.fillStyle = "rgba(170, 160, 210, 0.55)"; g.fillRect(90, 182, 332, 18);   // shaded underside
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  });
  return cloudTex;
}
/** inked painted cloud cards (sprites) spread over a sky band: x0..x1 at depth z, heights y0..y1 */
export function clouds(root: THREE.Object3D, o: { n?: number; x: [number, number]; y: [number, number]; z: [number, number]; size?: number; seed?: number; tint?: string }) {
  if (BARE) return;
  const r = rng(o.seed ?? 5), tx = cloudTextures();
  for (let i = 0; i < (o.n ?? 8); i++) {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: tx[i % 3], fog: false, transparent: true, depthWrite: false, color: o.tint ?? "#ffffff" }));
    const w = (o.size ?? 20) * (0.6 + r() * 0.8);
    s.scale.set(w, w / 2, 1);
    s.position.set(o.x[0] + r() * (o.x[1] - o.x[0]), o.y[0] + r() * (o.y[1] - o.y[0]), o.z[0] + r() * (o.z[1] - o.z[0]));
    s.layers.set(NOINK); s.renderOrder = -5; root.add(s);
  }
}
