// Character framing (our own code). Measured on frames30 sheets (docs/RND_LOG.md, "src/next parity pieces"): in the
// 24 references the lead character's head is a median 0.08 of the frame height when a character is on screen
// (per-video medians 0.035 / 0.08 / 0.25) and >= 0.07 in 47 % of all sampled frames; in Vasa v14 it is ~0.015 and
// never >= 0.07 - our figures are specks in wide shots. The refs stay close: two or three figures filling the lower
// half, the set behind them.
//   castKey(t, feet[], preset, az, el)  a solved framing that hits a head-size target:
//       "close"   one lead, chest up          head 0.20 of the frame height
//       "medium"  1-3 figures, knees up        head 0.11 (the refs' common two-shot)
//       "wide"    full bodies with the set     head 0.06 (still >= 0.04: never a speck)
//     heads land above the 0.64-0.78 caption band; bodies may run behind it, as in the refs.
//   headFrac(g, t, feet, scale)  projected head height / frame height of a figure at t in group g
//   castCheck(groups, castOf, words?)  per group: median of the largest head on screen; flags groups whose cast is
//     present but smaller than `min` (0.05) for more than half the group, and the overall share >= 0.07
import * as THREE from "three";
import { fit, type Box } from "../kit/framing";
import type { CamKey } from "../kit/campath";
import type { GroupSpec, V3 } from "../kit/Stage";
import { camAt, project, H } from "./match";

export type CastPreset = "close" | "medium" | "wide";
export const CAST_TARGET: Record<CastPreset, number> = { close: 0.2, medium: 0.11, wide: 0.06 };
const HEAD_C = 1.375, HEAD_R = 0.295;              // Person / Actor head centre and radius (m, scale 1)
const headBox = (p: V3, s = 1): Box => [p[0] - HEAD_R * s, p[1] + (HEAD_C - HEAD_R) * s, p[2] - 0.05, p[0] + HEAD_R * s, p[1] + (HEAD_C + HEAD_R) * s, p[2] + 0.05];

/** head height / frame height for a camera */
function headFracCam(cam: THREE.PerspectiveCamera, feet: V3, s = 1) {
  const a = project(cam, [feet[0], feet[1] + (HEAD_C + HEAD_R) * s, feet[2]]), b = project(cam, [feet[0], feet[1] + (HEAD_C - HEAD_R) * s, feet[2]]);
  if (a.behind || b.behind) return 0;
  const cx = (a.x + b.x) / 2, y0 = Math.min(a.y, b.y), y1 = Math.max(a.y, b.y);
  if (cx < 0 || cx > 1080 || y1 < 0 || y0 > H) return 0;                // off screen: not in the shot
  return (Math.min(y1, H) - Math.max(y0, 0)) / H;                      // the part of the head inside the frame
}
export const headFrac = (g: GroupSpec, t: number, feet: V3, s = 1) => headFracCam(camAt(g, t), feet, s);

const CAM = new THREE.PerspectiveCamera(40, 1080 / 1920, 0.05, 400);
/** a framing of the cast at the preset's size: solved with framing.fit, then dollied along the view line until the
 * biggest head hits the target; the heads are kept above the caption band */
/** bounds: a room the camera must stay inside (the dolly stops at its walls, 0.15 m in) */
export function castKey(t: number, feet: V3[], preset: CastPreset, az = 0, el = 6, fov = 36, s = 1, extra: Box[] = [], bounds?: Box): CamKey {
  const y0 = preset === "close" ? 0.95 : preset === "medium" ? 0.5 : 0;
  const boxes: Box[] = feet.map((p) => [p[0] - 0.32 * s, p[1] + y0 * s, p[2] - 0.12, p[0] + 0.32 * s, p[1] + 1.72 * s, p[2] + 0.12]);
  const pad = preset === "close" ? { t: 0.14, b: 0.62, x: 0.16 } : preset === "medium" ? { t: 0.18, b: 0.08, x: 0.08 } : { t: 0.22, b: 0.3, x: 0.08 };
  const k = fit(t, [...boxes, ...extra], az, el, fov, pad);
  const pos = new THREE.Vector3(...k.pos), look = new THREE.Vector3(...k.look);
  const target = CAST_TARGET[preset];
  const size = () => {
    CAM.fov = fov; CAM.aspect = 1080 / 1920; CAM.position.copy(pos); CAM.lookAt(look); CAM.updateProjectionMatrix(); CAM.updateMatrixWorld();
    return Math.max(...feet.map((f) => headFracCam(CAM, f, s)));
  };
  // dolly toward / away from the look point: head size goes as 1 / distance
  for (let i = 0; i < 6; i++) {
    const h = size(); if (h <= 0) break;
    const off = pos.clone().sub(look);
    let nd = Math.max(0.4, off.length() * (h / target));
    if (bounds) {
      const inB = (q: THREE.Vector3) => q.x > bounds[0] + 0.15 && q.y > bounds[1] && q.z > bounds[2] + 0.15 && q.x < bounds[3] - 0.15 && q.y < bounds[4] && q.z < bounds[5] - 0.15;
      while (nd > 0.4 && !inB(look.clone().add(off.clone().setLength(nd)))) nd *= 0.95;
    }
    pos.copy(look).add(off.setLength(nd));
  }
  // keep the heads above the caption band (head bottoms <= 0.62 of the height): tilt the look point down if needed
  for (let i = 0; i < 8; i++) {
    size();
    const low = Math.max(...feet.map((f) => project(CAM, [f[0], f[1] + (HEAD_C - HEAD_R) * s, f[2]]).y)) / H;
    if (low <= 0.6) break;
    look.y -= (low - 0.58) * pos.distanceTo(look) * 0.6;
  }
  return { t, pos: [pos.x, pos.y, pos.z], look: [look.x, look.y, look.z], fov };
}

export type CastReport = { group: string; frames: number; median: number; shareGe007: number; small: boolean }[];
/** the cast-size check over every group that has a cast (castOf returns the feet of the figures at t, or []) */
export function castCheck(groups: GroupSpec[], castOf: (g: GroupSpec, t: number) => V3[], fps = 30, min = 0.05) {
  const rows: CastReport = [];
  const all: number[] = [];
  for (const g of groups) {
    const hs: number[] = [];
    for (let f = Math.round(g.t0 * fps); f < Math.round(g.t1 * fps); f += 3) {
      const t = f / fps, feet = castOf(g, t);
      if (!feet.length) continue;
      const cam = camAt(g, t);
      hs.push(Math.max(...feet.map((p) => headFracCam(cam, p))));
    }
    if (!hs.length) continue;
    hs.sort((a, b) => a - b); all.push(...hs);
    const med = hs[Math.floor(hs.length / 2)];
    rows.push({ group: g.id, frames: hs.length, median: +med.toFixed(3), shareGe007: +(hs.filter((h) => h >= 0.07).length / hs.length).toFixed(2), small: med < min });
  }
  all.sort((a, b) => a - b);
  return { rows, median: all.length ? +all[Math.floor(all.length / 2)].toFixed(3) : 0, shareGe007: all.length ? +(all.filter((h) => h >= 0.07).length / all.length).toFixed(2) : 0,
    flagged: rows.filter((r) => r.small).map((r) => r.group) };
}
/** cast of a kit group: its visible people */
export const peopleCast = (g: GroupSpec, t: number): V3[] => g.people.filter((p) => !p.visible || p.visible(t)).map((p) => p.at(t));
export { headBox as castHeadBox };
