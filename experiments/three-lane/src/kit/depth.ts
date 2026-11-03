// Depth separation (our own code; visual track round 3, replication lesson 3: "everything equally sharp, practicals stay
// small glows"). Two pieces:
//   bokeh(points, o)        round bokeh discs on out-of-focus lights. Each point (a candle, a lamp, a window glint) gets
//                           a soft disc whose diameter follows the lens: k * cInf * |1 - focus / depth| px (the lens blur's
//                           own circle of confusion, scaled up, since the blur pass caps at 24 px); in focus it vanishes
//                           and the sharp flame shows. Discs are additive, NOINK, never bloomed.
//   foreground(make, o)     a foreground mass held in the near plane at a screen spot (a pillar edge, a jar shoulder, a
//                           drape), blurred by the lens; with from/to it crosses the frame as an in-world wipe
//   LENS_STATE              the current group's focus distance and blur strength (Stage writes it every frame)
import * as THREE from "three";
import { NOINK } from "../ink";
import type { Rig, V3 } from "./Stage";

export const LENS_STATE = { focus: 10, cInf: 12 };
const H = 1920;

let discTex: THREE.Texture | null = null;
function disc(): THREE.Texture {
  if (discTex) return discTex;
  const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d")!;
  const grd = g.createRadialGradient(64, 64, 0, 64, 64, 62);
  grd.addColorStop(0, "rgba(255,255,255,0.55)"); grd.addColorStop(0.78, "rgba(255,255,255,0.7)"); grd.addColorStop(0.9, "rgba(255,255,255,0.95)"); grd.addColorStop(1, "rgba(255,255,255,0)");
  g.fillStyle = grd; g.beginPath(); g.arc(64, 64, 62, 0, 7); g.fill();
  discTex = new THREE.CanvasTexture(c); discTex.colorSpace = THREE.SRGBColorSpace; return discTex;
}

export type BokehOpts = { color?: string; k?: number; max?: number; min?: number; gain?: number; visible?: (t: number) => boolean };
/** bokeh discs on the given world points (or a function of time returning them) */
export const bokeh = (points: V3[] | ((t: number) => V3[]), o: BokehOpts = {}): Rig => (ctx) => {
  const pts0 = typeof points === "function" ? points(0) : points;
  const col = new THREE.Color(o.color ?? "#ffc070");
  const sprites = pts0.map(() => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: disc(), color: col, blending: THREE.AdditiveBlending, depthWrite: false, fog: false, transparent: true, toneMapped: false }));
    s.layers.set(NOINK); ctx.root.add(s); return s;
  });
  const fwd = new THREE.Vector3(), p = new THREE.Vector3();
  return (t, cam) => {
    const pts = typeof points === "function" ? points(t) : points, show = o.visible ? o.visible(t) : true;
    cam.getWorldDirection(fwd);
    const tanH = Math.tan(((cam as THREE.PerspectiveCamera).fov * Math.PI) / 360);
    sprites.forEach((s, i) => {
      const q = pts[i]; if (!q || !show) { s.visible = false; return; }
      p.set(...q); const d = p.clone().sub(cam.position).dot(fwd);
      const coc = Math.min(o.max ?? 170, (o.k ?? 5) * LENS_STATE.cInf * Math.abs(1 - LENS_STATE.focus / Math.max(0.05, d)));
      if (d <= 0.1 || coc < (o.min ?? 8)) { s.visible = false; return; }
      s.visible = true; s.position.copy(p);
      const size = (coc / H) * 2 * d * tanH; s.scale.set(size, size, 1);
      // a big disc spreads the same light over more area: dimmer as it grows
      (s.material as THREE.SpriteMaterial).opacity = (o.gain ?? 1) * Math.min(0.9, 0.25 + 9 / Math.sqrt(coc));
    });
  };
};

/** a world point at screen (sx, sy) (0..1, y down) at distance `dist` along the view */
export function screenPoint(cam: THREE.Camera, sx: number, sy: number, dist: number, out = new THREE.Vector3()): THREE.Vector3 {
  const pc = cam as THREE.PerspectiveCamera, tanH = Math.tan((pc.fov * Math.PI) / 360), aspect = pc.aspect || 9 / 16;
  const v = new THREE.Vector3((sx - 0.5) * 2 * tanH * aspect * dist, -(sy - 0.5) * 2 * tanH * dist, -dist);
  return out.copy(v.applyMatrix4(cam.matrixWorld));
}
export type ForegroundOpts = { sx: number; sy: number; dist?: number; t0?: number; t1?: number; from?: [number, number]; to?: [number, number]; spin?: number };
/** hold an object in the near plane at a screen spot; between t0 and t1 it slides from `from` to `to` (a wipe) */
export const foreground = (make: () => THREE.Object3D, o: ForegroundOpts): Rig => (ctx) => {
  const obj = make(); ctx.root.add(obj);
  const p = new THREE.Vector3(), q = new THREE.Quaternion();
  return (t, cam) => {
    const inWin = (o.t0 === undefined || t >= o.t0) && (o.t1 === undefined || t <= o.t1);
    obj.visible = inWin; if (!inWin) return;
    let sx = o.sx, sy = o.sy;
    if (o.from && o.to && o.t0 !== undefined && o.t1 !== undefined) { const u = (t - o.t0) / (o.t1 - o.t0), e = u * u * (3 - 2 * u); sx = o.from[0] + (o.to[0] - o.from[0]) * e; sy = o.from[1] + (o.to[1] - o.from[1]) * e; }
    screenPoint(cam, sx, sy, o.dist ?? 0.9, p); obj.position.copy(p);
    cam.getWorldQuaternion(q); obj.quaternion.copy(q); if (o.spin) obj.rotateY(o.spin);
  };
};
