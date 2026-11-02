// Code-painted textures for story-vasa (our own designs): hull planking with the painted gun-port strakes, open water,
// the gilded stern (our own ornament: framed panels, two rampant lions as flat shapes, a sheaf crest), sail cloth,
// a Stockholm skyline strip (houses, spires, the castle tower), harbour mud and the sea bed.
import * as THREE from "three";
import { rng } from "../paint";

export function canvas(w: number, h: number): [HTMLCanvasElement, CanvasRenderingContext2D] {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  return [c, c.getContext("2d")!];
}
export const toTex = (c: HTMLCanvasElement, repeat: [number, number] = [1, 1]) => {
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...repeat); t.anisotropy = 8;
  return t;
};
const hsl = (h: number, s: number, l: number) => `hsl(${h}, ${s}%, ${l}%)`;

/** hull planking: horizontal strakes in dark oak, with a red-ochre band where the gun ports sit (v = height) */
export function hullPlanks(repeat: [number, number] = [6, 1], seed = 3) {
  const [c, g] = canvas(1024, 1024);
  const r = rng(seed);
  const rows = 34;
  for (let i = 0; i < rows; i++) {
    const y = (i / rows) * 1024, h = 1024 / rows;
    g.fillStyle = hsl(24 + r() * 6, 34 + r() * 8, 22 + r() * 7); g.fillRect(0, y, 1024, h);
    g.fillStyle = "rgba(8, 4, 2, 0.75)"; g.fillRect(0, y, 1024, 2);
    for (let k = 0; k < 3; k++) { const x = r() * 1024; g.fillRect(x, y, 2, h); }
    for (let k = 0; k < 4; k++) {
      g.strokeStyle = `rgba(0,0,0,${0.05 + r() * 0.08})`; g.lineWidth = 1 + r() * 1.5;
      const yy = y + 4 + r() * (h - 8); g.beginPath(); g.moveTo(0, yy); g.bezierCurveTo(300, yy + 3, 700, yy - 3, 1024, yy + 1); g.stroke();
    }
  }
  return toTex(c, repeat);
}

/** open water: teal-blue with painted wave dashes (scrolled by the story for motion) */
export function waterTex(repeat: [number, number] = [40, 40], seed = 5, deep = false) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = deep ? "#1f4f6e" : "#3f8fa6"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 26; i++) {
    const x = r() * 512, y = r() * 512, w = 40 + r() * 90;
    g.strokeStyle = deep ? "rgba(140, 200, 220, 0.35)" : "rgba(220, 245, 250, 0.55)"; g.lineWidth = 3 + r() * 3; g.lineCap = "round";
    g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + w / 2, y - 8, x + w, y); g.stroke();
  }
  for (let i = 0; i < 18; i++) {
    const x = r() * 512, y = r() * 512;
    g.fillStyle = deep ? "rgba(10, 40, 60, 0.35)" : "rgba(30, 90, 120, 0.35)";
    g.beginPath(); g.ellipse(x, y, 30 + r() * 50, 8 + r() * 10, 0, 0, Math.PI * 2); g.fill();
  }
  return toTex(c, repeat);
}

/** the gilded stern panel (our own ornament): framed tiers, two flat rampant lions, a sheaf crest, windows */
export function sternTex() {
  const [c, g] = canvas(512, 640);
  g.fillStyle = "#2f3f8c"; g.fillRect(0, 0, 512, 640);                     // blue ground
  const gold = "#e6b33c", goldD = "#a87618", red = "#b8352a";
  g.strokeStyle = gold; g.lineWidth = 14; g.strokeRect(10, 10, 492, 620);
  // window tier
  for (let i = 0; i < 4; i++) {
    g.fillStyle = gold; g.fillRect(52 + i * 108, 360, 84, 120);
    g.fillStyle = "#1a2350"; g.fillRect(62 + i * 108, 372, 64, 96);
    g.strokeStyle = gold; g.lineWidth = 4; g.beginPath(); g.moveTo(94 + i * 108, 372); g.lineTo(94 + i * 108, 468); g.stroke();
  }
  // crest: a gold sheaf on a red shield
  g.fillStyle = red; g.beginPath(); g.moveTo(196, 70); g.lineTo(316, 70); g.lineTo(316, 190); g.quadraticCurveTo(256, 250, 196, 190); g.closePath(); g.fill();
  g.strokeStyle = gold; g.lineWidth = 8; g.stroke();
  g.fillStyle = gold;
  for (let k = -2; k <= 2; k++) { g.save(); g.translate(256, 190); g.rotate(k * 0.18); g.fillRect(-5, -110, 10, 110); g.beginPath(); g.ellipse(0, -118, 9, 18, 0, 0, Math.PI * 2); g.fill(); g.restore(); }
  g.fillRect(226, 150, 60, 14);
  // two flat lions (own simple silhouettes), rampant toward the crest
  const lion = (x: number, flip: number) => {
    g.save(); g.translate(x, 200); g.scale(flip, 1); g.fillStyle = gold;
    g.beginPath(); g.ellipse(0, 0, 34, 54, -0.3, 0, Math.PI * 2); g.fill();          // body
    g.beginPath(); g.arc(24, -62, 30, 0, Math.PI * 2); g.fill();                         // mane
    g.fillStyle = goldD; g.beginPath(); g.arc(34, -60, 14, 0, Math.PI * 2); g.fill();     // face
    g.fillStyle = gold; g.fillRect(28, -30, 44, 12); g.fillRect(28, 10, 40, 12);         // paws
    g.fillRect(-26, 40, 14, 56); g.fillRect(4, 44, 14, 52);                              // legs
    g.strokeStyle = gold; g.lineWidth = 9; g.beginPath(); g.moveTo(-28, 10); g.quadraticCurveTo(-70, -10, -56, -60); g.stroke();   // tail
    g.restore();
  };
  lion(120, 1); lion(392, -1);
  // garlands
  g.strokeStyle = gold; g.lineWidth = 10;
  for (const y of [300, 520]) { g.beginPath(); g.moveTo(30, y); for (let x = 30; x <= 482; x += 64) g.quadraticCurveTo(x + 32, y + 26, x + 64, y); g.stroke(); }
  g.fillStyle = goldD; for (let x = 40; x < 480; x += 40) { g.beginPath(); g.arc(x, 580, 10, 0, Math.PI * 2); g.fill(); }
  return toTex(c);
}

/** sail cloth: cream panels with seams and a faint reef band */
export function sailTex(seed = 9) {
  const [c, g] = canvas(256, 256);
  const r = rng(seed);
  g.fillStyle = "#efe4c8"; g.fillRect(0, 0, 256, 256);
  for (let x = 0; x < 256; x += 32) { g.fillStyle = `rgba(150, 120, 80, ${0.12 + r() * 0.08})`; g.fillRect(x, 0, 2, 256); }
  g.fillStyle = "rgba(150, 120, 80, 0.2)"; g.fillRect(0, 40, 256, 3);
  return toTex(c);
}

/** a Stockholm skyline strip (our own drawing): gabled houses, two spires, the castle tower, on a rock */
export function skylineTex(seed = 11) {
  const [c, g] = canvas(2048, 512);
  const r = rng(seed);
  g.clearRect(0, 0, 2048, 512);
  g.fillStyle = "#6b6a72"; g.beginPath(); g.moveTo(0, 512); g.lineTo(0, 430); g.quadraticCurveTo(1024, 380, 2048, 440); g.lineTo(2048, 512); g.fill();
  const walls = ["#e7c58a", "#d98f62", "#c9b79a", "#e2a96b", "#b9806a", "#efd9a8"];
  let x = 20;
  while (x < 2000) {
    const w = 60 + r() * 70, h = 120 + r() * 110, y = 430 - h;
    g.fillStyle = walls[Math.floor(r() * walls.length)]; g.fillRect(x, y, w, h);
    g.fillStyle = r() < 0.5 ? "#8c3a2c" : "#5a5f7a"; g.beginPath(); g.moveTo(x - 4, y); g.lineTo(x + w / 2, y - 40 - r() * 30); g.lineTo(x + w + 4, y); g.fill();
    g.fillStyle = "#3c3550";
    for (let wy = y + 20; wy < 410; wy += 34) for (let wx = x + 10; wx < x + w - 14; wx += 22) g.fillRect(wx, wy, 10, 16);
    g.strokeStyle = "#2a2238"; g.lineWidth = 3; g.strokeRect(x, y, w, h);
    x += w + 4 + r() * 10;
  }
  const spire = (sx: number, h: number) => {
    g.fillStyle = "#c9b79a"; g.fillRect(sx - 26, 430 - h, 52, h);
    g.fillStyle = "#3f7a6a"; g.beginPath(); g.moveTo(sx - 30, 430 - h); g.lineTo(sx, 430 - h - 160); g.lineTo(sx + 30, 430 - h); g.fill();
    g.strokeStyle = "#2a2238"; g.lineWidth = 3; g.stroke(); g.strokeRect(sx - 26, 430 - h, 52, h);
  };
  spire(620, 230); spire(1380, 260);
  // the castle: a broad block with a round-topped tower
  g.fillStyle = "#e8dcc0"; g.fillRect(900, 190, 300, 240); g.strokeStyle = "#2a2238"; g.strokeRect(900, 190, 300, 240);
  g.fillStyle = "#5a5f7a"; g.fillRect(990, 70, 120, 120); g.beginPath(); g.arc(1050, 70, 60, Math.PI, 0); g.fill();
  g.fillStyle = "#e6b33c"; g.fillRect(1044, -2, 12, 30);
  return toTex(c);
}

/** soft mud / sea bed */
export function mudTex(repeat: [number, number] = [20, 20], seed = 13) {
  const [c, g] = canvas(512, 512);
  const r = rng(seed);
  g.fillStyle = "#4b5446"; g.fillRect(0, 0, 512, 512);
  for (let i = 0; i < 160; i++) {
    g.fillStyle = `rgba(${r() < 0.5 ? "30,36,30" : "110,120,96"}, ${0.15 + r() * 0.2})`;
    g.beginPath(); g.ellipse(r() * 512, r() * 512, 10 + r() * 40, 4 + r() * 12, r() * 3, 0, Math.PI * 2); g.fill();
  }
  return toTex(c, repeat);
}
