// Fire, smoke, embers and ash for the museum fire and the candle smoke (our own code). Flames are flat cartoon
// cards (layered coral / amber / cream tongues with an ink edge, like the 2D kit's flames) cut from an 8-frame
// sprite sheet so they flicker; smoke and embers are sprites. All on the NOINK layer, all deterministic in time.
import * as THREE from "three";
import { NOINK } from "../ink";
import { rng } from "../paint";

let sheet: HTMLCanvasElement | null = null;
const FR = 8;
function flameSheet() {
  if (sheet) return sheet;
  const c = document.createElement("canvas"); c.width = 128 * FR; c.height = 256;
  const g = c.getContext("2d")!;
  const tongue = (cx: number, base: number, w: number, h: number, sway: number, fill: string) => {
    g.fillStyle = fill; g.beginPath();
    g.moveTo(cx - w, base);
    g.bezierCurveTo(cx - w * 1.1, base - h * 0.45, cx - w * 0.3 + sway, base - h * 0.6, cx + sway * 1.4, base - h);
    g.bezierCurveTo(cx + w * 0.2 + sway, base - h * 0.55, cx + w * 1.15, base - h * 0.4, cx + w, base);
    g.closePath(); g.fill(); g.stroke();
  };
  g.lineJoin = "round"; g.strokeStyle = "#3a1208"; g.lineWidth = 3;
  for (let f = 0; f < FR; f++) {
    const x0 = f * 128 + 64, ph = (f / FR) * Math.PI * 2;
    tongue(x0, 250, 50, 220 + Math.sin(ph) * 18, Math.sin(ph) * 14, "#e8562e");
    tongue(x0 - 18, 250, 30, 150 + Math.cos(ph * 2) * 16, Math.cos(ph) * 10, "#f39a2e");
    tongue(x0 + 16, 250, 26, 130 + Math.sin(ph * 2 + 1) * 14, Math.sin(ph + 1) * 10, "#f39a2e");
    g.lineWidth = 0; g.strokeStyle = "rgba(0,0,0,0)";
    tongue(x0, 250, 16, 80 + Math.sin(ph * 3) * 10, Math.sin(ph) * 6, "#ffe9a8");
    g.strokeStyle = "#3a1208"; g.lineWidth = 3;
  }
  sheet = c;
  return c;
}
let smokeTex: THREE.Texture | null = null;
function smokeT() {
  if (smokeTex) return smokeTex;
  const c = document.createElement("canvas"); c.width = 128; c.height = 128;
  const g = c.getContext("2d")!;
  const grd = g.createRadialGradient(64, 64, 4, 64, 64, 62);
  grd.addColorStop(0, "rgba(70, 64, 92, 0.85)"); grd.addColorStop(0.7, "rgba(60, 56, 84, 0.45)"); grd.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
  smokeTex = new THREE.CanvasTexture(c); smokeTex.colorSpace = THREE.SRGBColorSpace;
  return smokeTex;
}
let puffTex: THREE.Texture | null = null;
function puffT() {
  if (puffTex) return puffTex;
  const c = document.createElement("canvas"); c.width = 128; c.height = 128;
  const g = c.getContext("2d")!;
  g.fillStyle = "#e6e2f0"; g.strokeStyle = "#1b1240"; g.lineWidth = 5;
  g.beginPath(); g.arc(64, 64, 52, 0, Math.PI * 2); g.fill(); g.stroke();
  puffTex = new THREE.CanvasTexture(c); puffTex.colorSpace = THREE.SRGBColorSpace;
  return puffTex;
}

let cells: THREE.CanvasTexture[] | null = null;
/** one texture per flicker frame (cut from the sheet, so no texture offsets are involved) */
function flameCells() {
  if (cells) return cells;
  const sh = flameSheet();
  cells = Array.from({ length: FR }, (_, f) => {
    const c = document.createElement("canvas"); c.width = 128; c.height = 256;
    c.getContext("2d")!.drawImage(sh, f * 128, 0, 128, 256, 0, 0, 128, 256);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
  });
  return cells;
}

export class Flame {
  readonly mesh: THREE.Mesh;
  private mat: THREE.MeshBasicMaterial;
  constructor(readonly size: number, readonly k: number) {
    this.mat = new THREE.MeshBasicMaterial({ map: flameCells()[0], alphaTest: 0.4, side: THREE.DoubleSide, fog: false });
    this.mesh = new THREE.Mesh(new THREE.PlaneGeometry(size * 0.5, size), this.mat);
    this.mesh.geometry.translate(0, size / 2, 0);
    this.mesh.layers.set(NOINK);
    this.mesh.frustumCulled = false;
  }
  update(t: number, grow: number, cam: THREE.Camera) {
    const f = Math.floor(t * 12 + this.k * 3) % FR;
    this.mat.map = flameCells()[f];
    const s = Math.max(0.001, grow);
    this.mesh.scale.set(s, s * (0.9 + 0.15 * Math.sin(t * 9 + this.k)), s);
    this.mesh.visible = grow > 0.02;
    this.mesh.quaternion.copy((cam as THREE.PerspectiveCamera).quaternion);
  }
}

/** rising sprites (smoke or embers or puffs) emitted from a point over time; deterministic per index */
export class Rising {
  readonly group = new THREE.Group();
  private sprites: THREE.Sprite[] = [];
  private seeds: number[][] = [];
  constructor(readonly n: number, readonly kind: "smoke" | "ember" | "puff", readonly scale: number, seed = 1) {
    const r = rng(seed);
    for (let i = 0; i < n; i++) {
      const mat = kind === "ember"
        ? new THREE.SpriteMaterial({ color: "#ffb35a", blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true })
        : new THREE.SpriteMaterial({ map: kind === "smoke" ? smokeT() : puffT(), depthWrite: false, fog: false, transparent: true });
      const s = new THREE.Sprite(mat); s.layers.set(NOINK); this.group.add(s); this.sprites.push(s);
      this.seeds.push([r(), r(), r(), r()]);
    }
  }
  /** amount 0..1; rise = height the particles climb over their life (m); life (s) */
  update(t: number, amount: number, rise: number, life: number, spread = 0.3) {
    this.sprites.forEach((s, i) => {
      const [a, b, c, d] = this.seeds[i];
      const age = ((t / life + a) % 1 + 1) % 1;
      s.visible = amount > 0.01;
      const sz = this.kind === "ember" ? this.scale * (0.4 + 0.6 * b) : this.scale * (0.5 + age * 1.6);
      s.scale.set(sz, sz, 1);
      s.position.set((c - 0.5) * spread + Math.sin((t + d * 6) * 1.7) * spread * 0.3 * age, age * rise, (b - 0.5) * spread * 0.5);
      (s.material as THREE.SpriteMaterial).opacity = amount * (this.kind === "ember" ? (1 - age) : Math.sin(age * Math.PI) * 0.85);
    });
  }
}

/** an ash heap (grows as the Turk burns away) */
export function ashHeap() {
  const m = new THREE.Mesh(new THREE.ConeGeometry(0.55, 0.35, 24), new THREE.MeshLambertMaterial({ color: "#2a2430" }));
  m.position.y = 0.175; m.castShadow = true; m.receiveShadow = true;
  return m;
}
