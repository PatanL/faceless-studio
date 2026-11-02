// Code-painted Canvas2D textures for the test set (our own code): wood planks with dark seams, warm plaster,
// red lacquer, a sky gradient for the window, and a rug. Seeded, so every frame and every machine paints the same.
import * as THREE from "three";

export const rng = (seed: number) => () => {
  seed |= 0; seed = (seed + 0x6d2b79f5) | 0;
  let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};

const canvas = (w: number, h: number) => {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  return [c, c.getContext("2d")!] as const;
};

const tex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => {
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(...repeat);
  t.anisotropy = 4;
  return t;
};

const hsl = (h: number, s: number, l: number) => `hsl(${h.toFixed(1)}, ${s.toFixed(1)}%, ${l.toFixed(1)}%)`;

/** Floor planks: rows of boards with staggered joints, per-board tone, grain streaks, dark soft seams. */
export function woodFloor(repeat: [number, number]) {
  const [c, g] = canvas(1024, 1024);
  const r = rng(7);
  const rowH = 128;
  for (let y = 0; y < 1024; y += rowH) {
    let x = -Math.floor(r() * 400);
    while (x < 1024) {
      const len = 300 + r() * 420;
      g.fillStyle = hsl(28 + r() * 8, 42 + r() * 12, 40 + r() * 9);
      g.fillRect(x, y, len, rowH);
      for (let k = 0; k < 14; k++) { // grain
        g.strokeStyle = `rgba(60, 30, 10, ${0.05 + r() * 0.08})`;
        g.lineWidth = 1 + r() * 3;
        const yy = y + 6 + r() * (rowH - 12);
        g.beginPath(); g.moveTo(x, yy);
        g.bezierCurveTo(x + len * 0.3, yy + (r() - 0.5) * 10, x + len * 0.7, yy + (r() - 0.5) * 10, x + len, yy + (r() - 0.5) * 6);
        g.stroke();
      }
      g.fillStyle = "rgba(45, 22, 10, 0.75)"; // end joint
      g.fillRect(x + len - 3, y, 5, rowH);
      x += len;
    }
    g.fillStyle = "rgba(45, 22, 10, 0.8)"; // long seam
    g.fillRect(0, y, 1024, 5);
  }
  return tex(c, repeat);
}

/** Warm plaster: flat base, low-frequency mottling, a few hairline cracks. */
export function plaster(repeat: [number, number]) {
  const [c, g] = canvas(512, 512);
  const r = rng(11);
  g.fillStyle = "#e6d2b0"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 120; i++) {
    const x = r() * 512, y = r() * 512, rad = 20 + r() * 90;
    const grd = g.createRadialGradient(x, y, 0, x, y, rad);
    const a = 0.03 + r() * 0.05;
    const dark = r() < 0.5;
    grd.addColorStop(0, dark ? `rgba(150, 110, 70, ${a})` : `rgba(255, 245, 225, ${a})`);
    grd.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = grd; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  g.strokeStyle = "rgba(110, 80, 50, 0.25)"; g.lineWidth = 1.2;
  for (let i = 0; i < 4; i++) {
    let x = r() * 512, y = r() * 512;
    g.beginPath(); g.moveTo(x, y);
    for (let k = 0; k < 8; k++) { x += (r() - 0.5) * 30; y += 8 + r() * 14; g.lineTo(x, y); }
    g.stroke();
  }
  return tex(c, repeat);
}

/** Red lacquer with faint vertical streaks (pillars, wainscot, window frame). */
export function lacquer(repeat: [number, number] = [1, 1]) {
  const [c, g] = canvas(256, 256);
  const r = rng(3);
  g.fillStyle = "#9b2a1e"; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 60; i++) {
    g.fillStyle = r() < 0.5 ? `rgba(60, 10, 5, ${0.05 + r() * 0.08})` : `rgba(220, 90, 60, ${0.04 + r() * 0.06})`;
    g.fillRect(r() * 256, 0, 1 + r() * 4, 256);
  }
  return tex(c, repeat);
}

/** Rug: deep red field, gold border, a simple lattice medallion. */
export function rug() {
  const [c, g] = canvas(1024, 768);
  g.fillStyle = "#7d1f22"; g.fillRect(0, 0, 1024, 768);
  g.strokeStyle = "#d6a640"; g.lineWidth = 26; g.strokeRect(40, 40, 944, 688);
  g.strokeStyle = "#2b3d6b"; g.lineWidth = 10; g.strokeRect(84, 84, 856, 600);
  g.save(); g.translate(512, 384); g.rotate(Math.PI / 4);
  g.strokeStyle = "#d6a640"; g.lineWidth = 12; g.strokeRect(-130, -130, 260, 260);
  g.fillStyle = "#2b3d6b"; g.fillRect(-70, -70, 140, 140);
  g.restore();
  return tex(c);
}

/** Sky seen through the window: cool blue overhead to the warm horizon colour. */
export function sky(top: string, horizon: string) {
  const [c, g] = canvas(64, 512);
  const grd = g.createLinearGradient(0, 0, 0, 512);
  grd.addColorStop(0, top); grd.addColorStop(0.75, horizon); grd.addColorStop(1, horizon);
  g.fillStyle = grd; g.fillRect(0, 0, 64, 512);
  const t = tex(c); t.wrapS = t.wrapT = THREE.ClampToEdgeWrapping;
  return t;
}

/** Soft contact-shadow blob (multiplied onto the floor): violet-dark centre to white. */
export function blob() {
  const [c, g] = canvas(256, 256);
  g.fillStyle = "#ffffff"; g.fillRect(0, 0, 256, 256);
  const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, "rgb(120, 112, 150)"); grd.addColorStop(0.45, "rgb(170, 164, 196)"); grd.addColorStop(1, "#ffffff");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
