// Hero-prop materials (our own code; visual track round 3, replication lesson 1: "hero props are primitives with flat
// two-tone gold"). Physically based metal, gold, bronze and glaze with specular highlights and environment reflections,
// kept inside the ink, lens and grade chain (they render on the world layer, so the ink pass outlines them).
//   metal("gold" | "bronze" | "darkBronze" | "silver" | "iron", { scales?, relief?, engrave?, rivets?, rough? })
//   engraveNormal(), rivetNormal(), reliefNormal(), scalesNormal(), grainNormal()   surface ornament as normal maps
//   glaze(color, { crackle? })                     glazed ceramic: a clear coat over a coloured body
//   applyEnv(root, renderer, mood)                 Stage calls this once per mounted set: every material that asked for
//                                                  reflections gets a shared PMREM environment ("candle" | "day" | "night")
// The environment is a painted room, not a photo: a gradient dome with a few bright warm "windows" and candle points,
// so gold catches small sharp highlights the way the references' lit gold does.
import * as THREE from "three";
import { rng } from "../paint";

const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };

// ---------------------------------------------------------------- normal maps painted as height, converted in place
function heightToNormal(h: Float32Array, W: number, H: number, strength: number): THREE.Texture {
  const [c, g] = canvas(W, H), img = g.createImageData(W, H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x, l = h[y * W + ((x - 1 + W) % W)], r = h[y * W + ((x + 1) % W)], u = h[((y - 1 + H) % H) * W + x], d = h[((y + 1) % H) * W + x];
    const nx = (l - r) * strength, ny = (d - u) * strength, nz = 1, L = Math.hypot(nx, ny, nz);
    img.data[i * 4] = (nx / L * 0.5 + 0.5) * 255; img.data[i * 4 + 1] = (ny / L * 0.5 + 0.5) * 255; img.data[i * 4 + 2] = (nz / L * 0.5 + 0.5) * 255; img.data[i * 4 + 3] = 255;
  }
  g.putImageData(img, 0, 0);
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4;
  return t;
}
const cache = new Map<string, THREE.Texture>();
/** overlapping round scales (dragon, fish, armour), as a tiling normal map */
export function scalesNormal(rows = 8): THREE.Texture {
  const key = `scales${rows}`; if (cache.has(key)) return cache.get(key)!;
  // rows of round scales drawn top to bottom, each covering the lower half of the row above (fish / dragon scales)
  const W = 256, H = 256, h = new Float32Array(W * H), s = W / rows, R = s * 0.62;
  for (let row = -1; row <= Math.ceil(H / (s * 0.5)) + 1; row++) {
    const cy = row * s * 0.5, off = (row % 2) * s * 0.5;
    for (let col = -1; col <= rows; col++) {
      const cx = col * s + off;
      for (let y = Math.floor(cy - R); y <= cy + R; y++) for (let x = Math.floor(cx - R); x <= cx + R; x++) {
        const q = Math.hypot(x - cx, y - cy) / R; if (q >= 1) continue;
        h[(((y % H) + H) % H) * W + (((x % W) + W) % W)] = Math.sqrt(1 - q * q) * (0.55 + 0.45 * Math.min(1, (y - cy + R) / (2 * R)));
      }
    }
  }
  const t = heightToNormal(h, W, H, 3.2); cache.set(key, t); return t;
}
/** a cast-relief band: meander (key fret) and bosses, for vessels and thrones */
export function reliefNormal(): THREE.Texture {
  if (cache.has("relief")) return cache.get("relief")!;
  const W = 256, H = 128, [c, g] = canvas(W, H);
  g.fillStyle = "#000"; g.fillRect(0, 0, W, H); g.strokeStyle = "#fff"; g.lineWidth = 7; g.lineCap = "square";
  for (let x = 0; x < W; x += 64) { g.beginPath(); g.moveTo(x + 6, 100); g.lineTo(x + 6, 28); g.lineTo(x + 54, 28); g.lineTo(x + 54, 82); g.lineTo(x + 24, 82); g.lineTo(x + 24, 46); g.lineTo(x + 40, 46); g.stroke(); }
  g.fillStyle = "#fff"; g.fillRect(0, 4, W, 6); g.fillRect(0, H - 10, W, 6);
  const d = g.getImageData(0, 0, W, H).data, h = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) h[i] = d[i * 4] / 255;
  // soften so the relief has rounded edges
  const b = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { let s = 0; for (let k = -2; k <= 2; k++) s += h[y * W + ((x + k + W) % W)] + h[((y + k + H) % H) * W + x]; b[y * W + x] = s / 10; }
  const t = heightToNormal(b, W, H, 2.4); cache.set("relief", t); return t;
}
/** fine hammered / cast-metal grain */
export function grainNormal(seed = 3): THREE.Texture {
  const key = `grain${seed}`; if (cache.has(key)) return cache.get(key)!;
  const W = 128, H = 128, h = new Float32Array(W * H), r = rng(seed);
  for (let k = 0; k < 160; k++) { const cx = r() * W, cy = r() * H, rad = 3 + r() * 9, a = (r() - 0.5) * 0.6;
    for (let y = -rad; y <= rad; y++) for (let x = -rad; x <= rad; x++) { const q = 1 - Math.hypot(x, y) / rad; if (q > 0) { const i = (((cy + y) | 0) + H) % H * W + ((((cx + x) | 0) + W) % W); h[i] += q * q * a; } } }
  const t = heightToNormal(h, W, H, 2.0); cache.set(key, t); return t;
}

/** engraved filigree: scrolls, curls and dots in a running band (worked metal, lacquer, carved wood) */
export function engraveNormal(): THREE.Texture {
  if (cache.has("engrave")) return cache.get("engrave")!;
  const W = 256, H = 128, [c, g] = canvas(W, H);
  g.fillStyle = "#000"; g.fillRect(0, 0, W, H); g.strokeStyle = "#fff"; g.lineWidth = 4; g.lineCap = "round";
  for (let x = 0; x < W; x += 64) {
    g.beginPath(); for (let k = 0; k <= 40; k++) { const a = k * 0.32, rr = 4 + k * 0.6; g.lineTo(x + 32 + Math.cos(a) * rr, 64 + Math.sin(a) * rr * 0.8); } g.stroke();
    g.beginPath(); g.moveTo(x, 64); g.bezierCurveTo(x + 16, 20, x + 48, 108, x + 64, 64); g.stroke();
    g.fillStyle = "#fff"; for (const [dx, dy] of [[8, 20], [56, 20], [8, 108], [56, 108]]) { g.beginPath(); g.arc(x + dx, dy, 4, 0, 7); g.fill(); }
  }
  g.fillRect(0, 4, W, 4); g.fillRect(0, H - 8, W, 4);
  const d = g.getImageData(0, 0, W, H).data, h = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) h[i] = d[i * 4] / 255;
  const t = heightToNormal(h, W, H, 2.2); cache.set("engrave", t); return t;
}
/** rivet rows on plates (armour, fittings, ship ironwork) */
export function rivetNormal(): THREE.Texture {
  if (cache.has("rivet")) return cache.get("rivet")!;
  const W = 128, H = 128, h = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const cx = (Math.floor(x / 32) + 0.5) * 32, cy = (Math.floor(y / 32) + 0.5) * 32, q = Math.hypot(x - cx, y - cy) / 7;
    h[y * W + x] = (q < 1 ? Math.sqrt(1 - q * q) : 0) + ((x % 64 < 2 || y % 64 < 2) ? -0.4 : 0);
  }
  const t = heightToNormal(h, W, H, 3); cache.set("rivet", t); return t;
}

// ---------------------------------------------------------------- materials
const METALS = {
  gold: { color: "#f2bf4a", rough: 0.28 }, bronze: { color: "#c98a46", rough: 0.36 }, darkBronze: { color: "#6f6a62", rough: 0.5 },
  silver: { color: "#d8dce4", rough: 0.25 }, iron: { color: "#7a7884", rough: 0.55 },
} as const;
export type MetalKind = keyof typeof METALS;
/** a real metal: specular highlights and environment reflections (the env arrives via applyEnv) */
export function metal(kind: MetalKind, o: { scales?: number; relief?: boolean; engrave?: boolean; rivets?: boolean; grain?: boolean; rough?: number; repeat?: [number, number]; color?: string } = {}): THREE.MeshStandardMaterial {
  const m = new THREE.MeshStandardMaterial({ color: o.color ?? METALS[kind].color, metalness: 1, roughness: o.rough ?? METALS[kind].rough });
  const nm = o.scales ? scalesNormal(o.scales) : o.engrave ? engraveNormal() : o.rivets ? rivetNormal() : o.relief ? reliefNormal() : o.grain !== false ? grainNormal(kind.length) : null;
  if (nm) { const t = nm.clone(); t.needsUpdate = true; t.repeat.set(...(o.repeat ?? [1, 1])); m.normalMap = t; m.normalScale.set(0.9, 0.9); }
  m.userData.env = true; m.envMapIntensity = 1.6;
  return m;
}
/** glazed ceramic or lacquer: a coloured, slightly rough body under a glossy clear coat */
export function glaze(color: string, o: { rough?: number; relief?: boolean } = {}): THREE.MeshPhysicalMaterial {
  const m = new THREE.MeshPhysicalMaterial({ color, metalness: 0, roughness: o.rough ?? 0.55, clearcoat: 1, clearcoatRoughness: 0.12 });
  if (o.relief) { m.normalMap = reliefNormal(); m.normalScale.set(0.7, 0.7); }
  m.userData.env = true; m.envMapIntensity = 0.9;
  return m;
}

// ---------------------------------------------------------------- the painted environment
export type EnvMood = "candle" | "day" | "night";
const envs = new Map<string, THREE.Texture>();
function envScene(mood: EnvMood): THREE.Scene {
  const s = new THREE.Scene(), r = rng(12);
  const [top, mid, bot] = mood === "candle" ? ["#a08466", "#6a5444", "#2e241e"] : mood === "night" ? ["#2a3060", "#141a3a", "#08081a"] : ["#cfe4ff", "#f2e6cf", "#6a5a48"];
  const [c, g] = canvas(64, 256), grd = g.createLinearGradient(0, 0, 0, 256);
  grd.addColorStop(0, top); grd.addColorStop(0.5, mid); grd.addColorStop(1, bot); g.fillStyle = grd; g.fillRect(0, 0, 64, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  s.add(new THREE.Mesh(new THREE.SphereGeometry(50, 32, 16), new THREE.MeshBasicMaterial({ map: t, side: THREE.BackSide })));
  // bright patches: windows / candles / sun, which become the gold's sharp highlights
  const spot = (col: string, k: number, w: number, h: number, az: number, el: number, d = 40) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(col).multiplyScalar(k), side: THREE.DoubleSide }));
    m.position.set(Math.sin(az) * Math.cos(el) * d, Math.sin(el) * d, Math.cos(az) * Math.cos(el) * d); m.lookAt(0, 0, 0); s.add(m);
  };
  if (mood === "candle") {
    for (let k = 0; k < 14; k++) spot("#ffb860", 6 + r() * 6, 1.2, 1.2, r() * Math.PI * 2, -0.1 + r() * 0.5);
    for (let k = 0; k < 6; k++) spot("#ffe0b0", 3.5, 6, 10, (k / 6) * Math.PI * 2 + 0.4, 0.35);
  } else if (mood === "night") {
    for (let k = 0; k < 6; k++) spot("#ffc070", 5, 1.5, 1.5, r() * Math.PI * 2, r() * 0.3);
    spot("#c8d4ff", 4, 6, 6, 1.0, 0.8);
  } else {
    spot("#fff4dc", 14, 10, 10, 0.8, 0.9); spot("#ffffff", 3, 30, 12, 2.5, 0.4);
  }
  return s;
}
/** give every material under root that asked for reflections the mood's PMREM environment */
export function applyEnv(root: THREE.Object3D, renderer: THREE.WebGLRenderer, mood: EnvMood = "candle") {
  let env = envs.get(mood);
  const need: THREE.MeshStandardMaterial[] = [];
  root.traverse((o) => { const m = (o as THREE.Mesh).material as THREE.MeshStandardMaterial | THREE.MeshStandardMaterial[] | undefined; if (!m) return; for (const x of Array.isArray(m) ? m : [m]) if (x.userData?.env && !x.envMap) need.push(x); });
  if (!need.length) return;
  if (!env) { const pm = new THREE.PMREMGenerator(renderer); env = pm.fromScene(envScene(mood), 0.02).texture; pm.dispose(); envs.set(mood, env); }
  for (const m of need) { m.envMap = env; m.needsUpdate = true; }
}
