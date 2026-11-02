// Screen-space helpers for the ghost-free joins (our own code): where a world point / quad / box lands on screen in
// a shot group at time t (the same CamPath the Stage flies), a solver that frames an anchor object at a given screen
// spot and size (match dissolves), portals for push-throughs, and the CSS homography that maps a full frame onto a
// prop's quad (frame-in-frame).
import * as THREE from "three";
import { CamPath, type CamKey } from "./campath";
import type { GroupSpec, V3 } from "./Stage";
import type { Box } from "./framing";

export const W = 1080, H = 1920;
const paths = new WeakMap<GroupSpec, CamPath>();
const CAM = new THREE.PerspectiveCamera(40, W / H, 0.05, 400);
const pathOf = (g: GroupSpec) => { let p = paths.get(g); if (!p) { p = new CamPath(g.cam, g.t0, g.t1); paths.set(g, p); } return p; };

/** the camera of group g at global time t (exactly as Stage poses it) */
export function camAt(g: GroupSpec, t: number, cam = CAM) {
  const c = pathOf(g).at(t);
  cam.fov = c.fov; cam.aspect = W / H; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  return cam;
}
/** screen px of a world point (behind = true when it is behind the lens) */
export function project(cam: THREE.PerspectiveCamera, p: V3): { x: number; y: number; behind: boolean } {
  const v = new THREE.Vector3(...p);
  const behind = v.clone().applyMatrix4(cam.matrixWorldInverse).z > -0.02;
  v.project(cam);
  return { x: (v.x * 0.5 + 0.5) * W, y: (0.5 - v.y * 0.5) * H, behind };
}
export const projectAt = (g: GroupSpec, t: number, p: V3) => project(camAt(g, t), p);
/** a world box's screen rectangle in group g at time t */
export function boxRect(g: GroupSpec, t: number, b: Box) {
  const cam = camAt(g, t);
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
  for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) {
    const q = project(cam, [x, y, z]);
    x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
  }
  return { x0, x1, y0, y1, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, h: y1 - y0, w: x1 - x0 };
}

/** a framing (CamKey at time t) that puts box b's screen rectangle centred on (cx, cy) with height h px, looking
 * along (az, el) degrees like framing.fit. Used to make the incoming shot of a match dissolve hold the anchor object
 * exactly where the outgoing shot left its anchor. */
export function matchKey(t: number, b: Box, target: { cx: number; cy: number; h: number }, az: number, el: number, fov = 40): CamKey {
  const c = new THREE.Vector3((b[0] + b[3]) / 2, (b[1] + b[4]) / 2, (b[2] + b[5]) / 2);
  const a = (az * Math.PI) / 180, e = (el * Math.PI) / 180;
  const dir = new THREE.Vector3(Math.sin(a) * Math.cos(e), Math.sin(e), Math.cos(a) * Math.cos(e));
  const look = c.clone();
  let d = new THREE.Vector3(b[3] - b[0], b[4] - b[1], b[5] - b[2]).length() * 2 + 0.3;
  CAM.fov = fov; CAM.aspect = W / H; CAM.updateProjectionMatrix();
  const right = new THREE.Vector3(), up = new THREE.Vector3();
  for (let i = 0; i < 60; i++) {
    CAM.position.copy(look).addScaledVector(dir, d); CAM.lookAt(look); CAM.updateMatrixWorld();
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (const x of [b[0], b[3]]) for (const y of [b[1], b[4]]) for (const z of [b[2], b[5]]) {
      const q = project(CAM, [x, y, z]); x0 = Math.min(x0, q.x); x1 = Math.max(x1, q.x); y0 = Math.min(y0, q.y); y1 = Math.max(y1, q.y);
    }
    const halfH = d * Math.tan((fov * Math.PI) / 360), pxPerM = H / (2 * halfH);
    right.setFromMatrixColumn(CAM.matrixWorld, 0); up.setFromMatrixColumn(CAM.matrixWorld, 1);
    // move the look point so the box centre lands on the target, scale the distance so the height matches
    look.addScaledVector(right, (((x0 + x1) / 2 - target.cx) / pxPerM) * 0.7).addScaledVector(up, (-((y0 + y1) / 2 - target.cy) / pxPerM) * 0.7);
    d *= 1 + ((y1 - y0) / target.h - 1) * 0.6;
  }
  CAM.position.copy(look).addScaledVector(dir, d);
  return { t, pos: [CAM.position.x, CAM.position.y, CAM.position.z], look: [look.x, look.y, look.z], fov, drift: 0.4 };
}

export type Shape = { kind: "poly"; pts: [number, number][] } | { kind: "circle"; cx: number; cy: number; r: number } | { kind: "full" };
/** a window / screen / photo opening in group g (corners in order TL, TR, BR, BL): its screen polygon at t,
 * or "full" once a corner passes behind the lens (the camera is through) */
export const quadPortal = (g: GroupSpec, quad: V3[]) => (t: number): Shape => {
  const cam = camAt(g, t);
  const pts = quad.map((p) => project(cam, p));
  if (pts.some((p) => p.behind)) return { kind: "full" };
  return { kind: "poly", pts: pts.map((p) => [p.x, p.y]) };
};
/** a round opening (a pupil, a porthole, a spyglass) of world radius r facing the camera, centred at c(t) */
export const circlePortal = (g: GroupSpec, c: (t: number) => V3, r: number) => (t: number): Shape => {
  const cam = camAt(g, t);
  const p = project(cam, c(t));
  if (p.behind) return { kind: "full" };
  const dist = cam.position.distanceTo(new THREE.Vector3(...c(t)));
  const rpx = (r / (2 * dist * Math.tan((cam.fov * Math.PI) / 360))) * H;
  return { kind: "circle", cx: p.x, cy: p.y, r: rpx };
};
/** does a shape cover the whole frame? */
export function covers(s: Shape): boolean {
  if (s.kind === "full") return true;
  const corners: [number, number][] = [[0, 0], [W, 0], [W, H], [0, H]];
  if (s.kind === "circle") return corners.every(([x, y]) => Math.hypot(x - s.cx, y - s.cy) <= s.r);
  return corners.every(([x, y]) => inPoly(s.pts, x, y));
}
function inPoly(p: [number, number][], x: number, y: number) {
  let ins = false;
  for (let i = 0, j = p.length - 1; i < p.length; j = i++) {
    const [xi, yi] = p[i], [xj, yj] = p[j];
    if ((yi > y) !== (yj > y) && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) ins = !ins;
  }
  return ins;
}
/** CSS clip-path for a shape */
export function clipCss(s: Shape): string | undefined {
  if (s.kind === "full") return undefined;
  if (s.kind === "circle") return `circle(${s.r.toFixed(1)}px at ${s.cx.toFixed(1)}px ${s.cy.toFixed(1)}px)`;
  return `polygon(${s.pts.map(([x, y]) => `${x.toFixed(1)}px ${y.toFixed(1)}px`).join(", ")})`;
}

/** CSS matrix3d mapping the full frame (0,0)-(W,H) onto quad [TL, TR, BR, BL] (transform-origin 0 0) */
export function homography(q: [number, number][]): string {
  const src: [number, number][] = [[0, 0], [W, 0], [W, H], [0, H]];
  // solve the 8 unknowns of the projective map src -> dst
  const A: number[][] = [], bv: number[] = [];
  for (let i = 0; i < 4; i++) {
    const [x, y] = src[i], [u, v] = q[i];
    A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); bv.push(u);
    A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); bv.push(v);
  }
  const h = solve8(A, bv);
  const [a, b, c, d, e, f, g, hh] = h;
  // matrix3d is column-major: [a d 0 g; b e 0 h; 0 0 1 0; c f 0 1] in the CSS 4x4 layout
  const m = [a, d, 0, g, b, e, 0, hh, 0, 0, 1, 0, c, f, 0, 1];
  return `matrix3d(${m.map((x) => x.toFixed(9)).join(",")})`;
}
function solve8(A: number[][], b: number[]) {
  const n = 8, M = A.map((r, i) => [...r, b[i]]);
  for (let i = 0; i < n; i++) {
    let p = i; for (let r = i + 1; r < n; r++) if (Math.abs(M[r][i]) > Math.abs(M[p][i])) p = r;
    [M[i], M[p]] = [M[p], M[i]];
    for (let r = 0; r < n; r++) if (r !== i) { const k = M[r][i] / M[i][i]; for (let c = i; c <= n; c++) M[r][c] -= k * M[i][c]; }
  }
  return M.map((r, i) => r[n] / r[i]);
}
/** a world quad's screen corners in group g at t (for frame-in-frame props) */
export const quadAt = (g: GroupSpec, quad: V3[]) => (t: number): [number, number][] => { const cam = camAt(g, t); return quad.map((p) => { const q = project(cam, p); return [q.x, q.y]; }); };
