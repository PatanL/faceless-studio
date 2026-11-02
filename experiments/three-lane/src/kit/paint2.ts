// More code-painted Canvas2D textures for the story-chess-turk sets (our own code): courtyard stone, marble checker,
// palace wall, parchment, night sky, brass, gears, the museum sign. Seeded like paint.ts, so every frame and every
// machine paints the same.
import * as THREE from "three";
import { rng } from "../paint";

const canvas = (w: number, h: number) => {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  return [c, c.getContext("2d")!] as const;
};
export const tex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => {
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(...repeat);
  t.anisotropy = 4;
  return t;
};
const hsl = (h: number, s: number, l: number, a = 1) => `hsla(${h.toFixed(1)}, ${s.toFixed(1)}%, ${l.toFixed(1)}%, ${a})`;

/** courtyard / street paving: irregular stone setts with dark gaps */
export function paving(repeat: [number, number], hue = 36, light = 70, seed = 5) {
  const [c, g] = canvas(1024, 1024);
  const r = rng(seed);
  g.fillStyle = hsl(hue, 14, light - 22); g.fillRect(0, 0, 1024, 1024);
  const row = 96;
  for (let y = 0; y < 1024; y += row) {
    let x = -r() * 120;
    while (x < 1024) {
      const w = 110 + r() * 90;
      g.fillStyle = hsl(hue + (r() - 0.5) * 10, 12 + r() * 10, light - 6 + r() * 10);
      g.beginPath();
      g.roundRect(x + 4, y + 4, w - 8, row - 8, 14);
      g.fill();
      for (let k = 0; k < 6; k++) {
        g.fillStyle = `rgba(80, 60, 40, ${0.04 + r() * 0.05})`;
        g.beginPath(); g.arc(x + r() * w, y + r() * row, 6 + r() * 18, 0, Math.PI * 2); g.fill();
      }
      x += w;
    }
  }
  return tex(c, repeat);
}

/** palace facade stucco (warm yellow) with faint horizontal coursing */
export function stucco(repeat: [number, number], base = "#e9c66a", seed = 13) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 90; i++) {
    const x = r() * 512, y = r() * 512, rad = 20 + r() * 80;
    const grd = g.createRadialGradient(x, y, 0, x, y, rad);
    grd.addColorStop(0, r() < 0.5 ? "rgba(150,100,40,0.05)" : "rgba(255,245,215,0.06)");
    grd.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = grd; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  g.fillStyle = "rgba(120, 80, 30, 0.18)";
  for (let y = 0; y < 512; y += 64) g.fillRect(0, y, 512, 3);
  return tex(c, repeat);
}

/** black and white marble floor tiles with veins and dark grout */
export function marbleChecker(repeat: [number, number], a = "#efe8dc", b = "#3b3a4a", seed = 21) {
  const [c, g] = canvas(1024, 1024);
  const r = rng(seed);
  const n = 4, s = 1024 / n;
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    g.fillStyle = (i + j) % 2 ? b : a; g.fillRect(i * s, j * s, s, s);
    g.strokeStyle = (i + j) % 2 ? "rgba(255,255,255,0.08)" : "rgba(90,80,100,0.18)";
    g.lineWidth = 2;
    for (let k = 0; k < 3; k++) {
      g.beginPath(); let x = i * s + r() * s, y = j * s;
      g.moveTo(x, y);
      for (let q = 0; q < 6; q++) { x += (r() - 0.5) * 60; y += s / 6; g.lineTo(x, y); }
      g.stroke();
    }
  }
  g.strokeStyle = "rgba(30, 25, 30, 0.6)"; g.lineWidth = 6;
  for (let i = 0; i <= n; i++) { g.beginPath(); g.moveTo(i * s, 0); g.lineTo(i * s, 1024); g.stroke(); g.beginPath(); g.moveTo(0, i * s); g.lineTo(1024, i * s); g.stroke(); }
  return tex(c, repeat);
}

/** painted wall panel colour with a darker frame and mottling (salon, workshop, museum interior) */
export function panelWall(repeat: [number, number], base: string, frame: string, seed = 31) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 70; i++) {
    const x = r() * 512, y = r() * 512, rad = 20 + r() * 70;
    const grd = g.createRadialGradient(x, y, 0, x, y, rad);
    grd.addColorStop(0, r() < 0.5 ? "rgba(0,0,0,0.05)" : "rgba(255,255,255,0.05)");
    grd.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = grd; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  g.strokeStyle = frame; g.lineWidth = 14; g.strokeRect(40, 60, 432, 392);
  g.lineWidth = 4; g.strokeRect(58, 78, 396, 356);
  return tex(c, repeat);
}

/** rough stone wall: blocks with mortar (workshop, museum) */
export function stoneWall(repeat: [number, number], hue = 225, light = 34, seed = 41) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = hsl(hue, 10, light - 12); g.fillRect(0, 0, 512, 512);
  const rowH = 64;
  for (let y = 0, k = 0; y < 512; y += rowH, k++) {
    let x = k % 2 ? -64 : 0;
    while (x < 512) {
      const w = 100 + r() * 60;
      g.fillStyle = hsl(hue + (r() - 0.5) * 12, 8 + r() * 8, light + (r() - 0.5) * 8);
      g.fillRect(x + 3, y + 3, w - 6, rowH - 6);
      x += w;
    }
  }
  return tex(c, repeat);
}

/** dark wood boards (workshop floor, ceilings) */
export function darkBoards(repeat: [number, number], seed = 51) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  for (let x = 0; x < 512; x += 64) {
    g.fillStyle = hsl(25 + r() * 6, 30 + r() * 10, 20 + r() * 7); g.fillRect(x, 0, 64, 512);
    g.fillStyle = "rgba(10, 5, 2, 0.8)"; g.fillRect(x, 0, 4, 512);
    for (let k = 0; k < 8; k++) {
      g.strokeStyle = `rgba(0,0,0,${0.06 + r() * 0.08})`; g.lineWidth = 1 + r() * 2;
      const xx = x + 6 + r() * 52; g.beginPath(); g.moveTo(xx, 0); g.bezierCurveTo(xx + 6, 170, xx - 6, 340, xx + 3, 512); g.stroke();
    }
  }
  return tex(c, repeat);
}

/** cabinet wood: warm boards with grain and a darker edge band */
export function cabinetWood(repeat: [number, number] = [1, 1], seed = 61) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = "#b47a3a"; g.fillRect(0, 0, 512, 512);
  for (let k = 0; k < 70; k++) {
    g.strokeStyle = `rgba(80, 40, 10, ${0.05 + r() * 0.1})`; g.lineWidth = 1 + r() * 3;
    const y = r() * 512; g.beginPath(); g.moveTo(0, y);
    g.bezierCurveTo(170, y + (r() - 0.5) * 30, 340, y + (r() - 0.5) * 30, 512, y + (r() - 0.5) * 10); g.stroke();
  }
  return tex(c, repeat);
}

/** brass (gears, knobs, frames): warm gold with a soft streak */
export function brass() {
  const [c, g] = canvas(128, 128);
  const grd = g.createLinearGradient(0, 0, 128, 128);
  grd.addColorStop(0, "#f2c75a"); grd.addColorStop(0.5, "#d9a43a"); grd.addColorStop(1, "#f6d27a");
  g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
  return tex(c);
}

/** parchment for the touring map: warm paper, darker edges, stains */
export function parchment(seed = 71) {
  const [c, g] = canvas(1024, 1024);
  const r = rng(seed);
  g.fillStyle = "#ecd8a8"; g.fillRect(0, 0, 1024, 1024);
  for (let i = 0; i < 80; i++) {
    const x = r() * 1024, y = r() * 1024, rad = 30 + r() * 140;
    const grd = g.createRadialGradient(x, y, 0, x, y, rad);
    grd.addColorStop(0, `rgba(150, 100, 40, ${0.03 + r() * 0.05})`); grd.addColorStop(1, "rgba(0,0,0,0)");
    g.fillStyle = grd; g.fillRect(x - rad, y - rad, rad * 2, rad * 2);
  }
  const edge = g.createRadialGradient(512, 512, 380, 512, 512, 760);
  edge.addColorStop(0, "rgba(0,0,0,0)"); edge.addColorStop(1, "rgba(110, 60, 20, 0.45)");
  g.fillStyle = edge; g.fillRect(0, 0, 1024, 1024);
  return c;
}

/** a text sign (museum, shop): letters on a board; the caller makes sure the font is loaded */
export function signTex(text: string, w: number, h: number, bg: string, fg: string, font = '"Anton", Impact, sans-serif') {
  const [c, g] = canvas(w, h);
  g.fillStyle = bg; g.fillRect(0, 0, w, h);
  g.strokeStyle = fg; g.lineWidth = Math.max(4, h * 0.05); g.strokeRect(h * 0.08, h * 0.08, w - h * 0.16, h - h * 0.16);
  g.fillStyle = fg; g.textAlign = "center"; g.textBaseline = "middle";
  g.font = `${Math.round(h * 0.58)}px ${font}`;
  (g as CanvasRenderingContext2D & { letterSpacing?: string }).letterSpacing = `${Math.round(h * 0.06)}px`;
  g.fillText(text, w / 2, h * 0.53);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return t;
}

/** vertical sky gradient (day, dusk or night with stars) */
export function skyGrad(top: string, mid: string, bottom: string, stars = 0, seed = 81) {
  const [c, g] = canvas(256, 1024);
  const grd = g.createLinearGradient(0, 0, 0, 1024);
  grd.addColorStop(0, top); grd.addColorStop(0.55, mid); grd.addColorStop(1, bottom);
  g.fillStyle = grd; g.fillRect(0, 0, 256, 1024);
  const r = rng(seed);
  for (let i = 0; i < stars; i++) {
    g.fillStyle = `rgba(255, 250, 235, ${0.4 + r() * 0.6})`;
    g.beginPath(); g.arc(r() * 256, r() * 600, 0.8 + r() * 1.6, 0, Math.PI * 2); g.fill();
  }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

/** soft radial glow for additive light pools (candles, windows, fire) */
export function glow(rgb: [number, number, number]) {
  const [c, g] = canvas(256, 256);
  const grd = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  grd.addColorStop(0, `rgba(${rgb.join(",")}, 1)`); grd.addColorStop(0.3, `rgba(${rgb.join(",")}, 0.45)`);
  grd.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  return t;
}
