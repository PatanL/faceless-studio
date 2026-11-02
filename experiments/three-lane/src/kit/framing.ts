// Story-lane helpers (our own code): eased tracks for story files, and solved framings.
// fit() puts the camera where every subject box fits the 9:16 frame with margins (the bottom margin keeps subjects
// above the caption band), pulls in or avoids other figures so no held framing cuts one at the edge, and keeps the
// camera inside the room set with setRoom().
import * as THREE from "three";
import type { V3 } from "./Stage";
import type { CamKey } from "./campath";
import { NOINK } from "../ink";

export const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
export const sm = (u: number) => { u = clamp01(u); return u * u * (3 - 2 * u); };
/** eased ramp from v0 at t0 to v1 at t1 */
export const ramp = (t: number, t0: number, t1: number, v0: number, v1: number) => v0 + (v1 - v0) * sm((t - t0) / Math.max(1e-6, t1 - t0));
/** piecewise eased track [[t, v], ...] */
export const track = (t: number, keys: [number, number][]) => {
  if (t <= keys[0][0]) return keys[0][1];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) return ramp(t, keys[i - 1][0], keys[i][0], keys[i - 1][1], keys[i][1]);
  return keys[keys.length - 1][1];
};
/** discrete value held from each key time */
export const step = <T,>(t: number, keys: [number, T][]): T => { let v = keys[0][1]; for (const [k, x] of keys) if (t >= k) v = x; return v; };
/** poses as a stick-kit track (the Person blends pose changes over 0.22 s itself): pass absolute times */
export const poses = (keys: [number, string][]) => keys.map(([t, v]) => ({ t, v }));
export const K = (t: number, pos: V3, look: V3, fov = 40): CamKey => ({ t, pos, look, fov });
/** move along keyframes [[t, x, z], ...] (eased), y = 0 */
export const walk = (t: number, keys: [number, number, number][]): V3 => {
  if (t <= keys[0][0]) return [keys[0][1], 0, keys[0][2]];
  for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) {
    const u = sm((t - keys[i - 1][0]) / (keys[i][0] - keys[i - 1][0]));
    return [keys[i - 1][1] + (keys[i][1] - keys[i - 1][1]) * u, 0, keys[i - 1][2] + (keys[i][2] - keys[i - 1][2]) * u];
  }
  const l = keys[keys.length - 1]; return [l[1], 0, l[2]];
};
export const walking = (t: number, keys: [number, number, number][]) => {
  for (let i = 1; i < keys.length; i++) if (t >= keys[i - 1][0] && t < keys[i][0] && (keys[i][1] !== keys[i - 1][1] || keys[i][2] !== keys[i - 1][2])) return 1;
  return 0;
};


// ------------------------------------------------------------------------------------------------ framing
/** an axis-aligned box [x0, y0, z0, x1, y1, z1] (world metres) that a shot must hold */
export type Box = [number, number, number, number, number, number];
/** a figure standing (or seated) with its feet at p (p[1] = the floor it stands on); upper = from the chest up */
export const personBox = (p: V3, seated = false, upper = false): Box =>
  [p[0] - 0.32, p[1] + (upper ? (seated ? 0.75 : 0.95) : 0), p[2] - 0.12, p[0] + 0.32, p[1] + (seated ? 1.45 : 1.7), p[2] + 0.12];
const FIT_CAM = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.05, 200);
export type Pad = { x?: number; t?: number; b?: number };
const corners = (boxes: Box[]) => {
  const pts: THREE.Vector3[] = [];
  for (const b of boxes) for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) pts.push(new THREE.Vector3(x, y, z));
  return pts;
};
function solve(boxes: Box[], az: number, el: number, fov: number, pad: Pad) {
  const px = pad.x ?? 0.12, pt = pad.t ?? 0.14, pb = pad.b ?? 0.3;
  const pts = corners(boxes);
  const bb = new THREE.Box3().setFromPoints(pts);
  const look = bb.getCenter(new THREE.Vector3());
  const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180;
  const dir = new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e));
  let d = bb.getSize(new THREE.Vector3()).length() * 1.5 + 0.5;
  const cam = FIT_CAM; cam.fov = fov; cam.updateProjectionMatrix();
  const right = new THREE.Vector3(), up = new THREE.Vector3();
  for (let i = 0; i < 40; i++) {
    cam.position.copy(look).addScaledVector(dir, d); cam.lookAt(look); cam.updateMatrixWorld();
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, behind = false;
    for (const p of pts) {
      const v = p.clone().applyMatrix4(cam.matrixWorldInverse);
      if (v.z > -0.1) { behind = true; break; }
      const q = p.clone().project(cam);
      x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
    }
    if (behind) { d *= 1.4; continue; }
    const tx0 = -1 + px, tx1 = 1 - px, ty0 = -1 + pb, ty1 = 1 - pt;
    const s = Math.max((x1 - x0) / (tx1 - tx0), (y1 - y0) / (ty1 - ty0));
    const halfH = d * Math.tan((fov * Math.PI) / 360), halfW = halfH * (1080 / 1920);
    right.setFromMatrixColumn(cam.matrixWorld, 0); up.setFromMatrixColumn(cam.matrixWorld, 1);
    look.addScaledVector(right, (((x0 + x1) / 2 - (tx0 + tx1) / 2) * halfW) * 0.8).addScaledVector(up, (((y0 + y1) / 2 - (ty0 + ty1) / 2) * halfH) * 0.8);
    d *= 1 + (s - 1) * 0.7;
  }
  cam.position.copy(look).addScaledVector(dir, d); cam.lookAt(look); cam.updateMatrixWorld();
  return { pos: cam.position.clone(), look };
}
/** fraction of a box's screen rectangle inside the frame for the last solved camera (0 when behind the lens) */
export function inside(b: Box) {
  const cam = FIT_CAM;
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  const cs = corners([b]);
  const zs = cs.map((p) => p.clone().applyMatrix4(cam.matrixWorldInverse).z);
  if (zs.every((z) => z > -0.05)) return 0;              // wholly behind the camera
  for (const p of cs) {
    const v = p.clone().applyMatrix4(cam.matrixWorldInverse);
    if (v.z > -0.05) return 0.5;          // straddles the lens: treat as cut
    const q = p.clone().project(cam);
    x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
  }
  const ix = Math.max(0, Math.min(1, x1) - Math.max(-1, x0)), iy = Math.max(0, Math.min(1, y1) - Math.max(-1, y0));
  return (ix * iy) / Math.max(1e-6, (x1 - x0) * (y1 - y0));
}
/** a checked framing: the camera looks along (az, el) degrees (az 0 = from the front, +z; az 90 = from +x; el > 0 =
 * from above) and stands where every box fits inside the 9:16 frame with the given margins (NDC units; the bottom
 * margin keeps the subjects above the caption band). others: the other figures in the place - a figure that would be
 * cut by the frame edge is taken into the shot when it is mostly in, and the angle is nudged when only a sliver of it
 * shows, so no held framing cuts a figure */
/** the room the camera must stay inside for the fits that follow (null = open air) */
let ROOM: Box | null = null;
export const setRoom = (b: Box | null) => { ROOM = b; };
const inRoom = (p: THREE.Vector3) => !ROOM || (p.x > ROOM[0] && p.y > ROOM[1] && p.z > ROOM[2] && p.x < ROOM[3] && p.y < ROOM[4] && p.z < ROOM[5]);
export function fit(t: number, boxes: Box[], az: number, el: number, fov = 40, pad: Pad = {}, others: Box[] = []): CamKey {
  // inside a room: widen the lens, then swing toward the front, until the camera stands inside it
  for (const [dz, df] of [[0, 0], [0, 8], [0, 16], [Math.sign(az) * -15, 8], [Math.sign(az) * -30, 8], [Math.sign(az) * -45, 8]]) {
    const k = fitFree(t, boxes, az + dz, el, fov + df, pad, others);
    if (inRoom(new THREE.Vector3(...k.pos))) return k;
  }
  return fitFree(t, boxes, 0, el, fov + 16, pad, others);
}
function fitFree(t: number, boxes: Box[], az: number, el: number, fov = 40, pad: Pad = {}, others: Box[] = []): CamKey {
  let subj = [...boxes];
  let best: { pos: THREE.Vector3; look: THREE.Vector3; bad: number } | null = null;
  for (const daz of [0, 6, -6, 12, -12, 18, -18]) {
    subj = [...boxes];
    let r = solve(subj, az + daz, el, fov, pad);
    for (let k = 0; k < 4; k++) {
      const grow = others.filter((b) => { const f = inside(b); return f > 0.3 && f < 0.995 && !subj.includes(b); });
      if (!grow.length) break;
      subj.push(...grow); r = solve(subj, az + daz, el, fov, pad);
    }
    const bad = others.filter((b) => !subj.includes(b)).reduce((n, b) => { const f = inside(b); return n + (f > 0.002 && f < 0.995 ? 1 : 0); }, 0);
    if (!best || bad < best.bad) best = { ...r, bad };
    if (bad === 0) break;
  }
  const { pos, look } = best!;
  return { t, pos: [pos.x, pos.y, pos.z], look: [look.x, look.y, look.z], fov };
}
/** shift a box by a cabinet position */
export const at = (c: V3, b: Box): Box => [b[0] + c[0], b[1] + c[1], b[2] + c[2], b[3] + c[0], b[4] + c[1], b[5] + c[2]];


/** a 3D text tag (lantern-tag look: dark pill, cream Anton text) that lives in the world (moves with the camera) */
export function tagSprite(text: string, h = 0.07) {
  const c = document.createElement("canvas");
  const g = c.getContext("2d")!;
  g.font = '64px "Anton", Impact, sans-serif';
  const w = Math.ceil(g.measureText(text).width) + 90;
  c.width = w; c.height = 110;
  g.fillStyle = "rgba(27, 18, 64, 0.92)"; g.beginPath(); g.roundRect(4, 4, w - 8, 102, 51); g.fill();
  g.strokeStyle = "#f2d8a0"; g.lineWidth = 5; g.stroke();
  g.fillStyle = "#fff2c0"; g.font = '64px "Anton", Impact, sans-serif'; g.textBaseline = "middle"; g.textAlign = "center";
  (g as CanvasRenderingContext2D & { letterSpacing?: string }).letterSpacing = "3px";
  g.fillText(text, w / 2, 58);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: t, depthTest: false, fog: false, transparent: true }));
  s.scale.set(h * (w / 110), h, 1); s.layers.set(NOINK); s.renderOrder = 10;
  s.userData.minPx = 64;          // never shorter than 64 px on a 1920 frame (text cap ~36 px; Vasa panel: labels too small)
  return s;
}
