// Framing check for the 3D story (our own code): replays every frame's camera from story.ts (pure math, no render)
// and reports figures cut by the frame edge, figures looming in front of the lens, the cabinet cut by the edge and
// the caption band over the cabinet. Run: node scripts/framing.mjs <storyboard.json> (bundled with esbuild).
import fs from "fs";
import * as THREE from "three";
import { Timing } from "../src/turk/timing";
import { buildStory } from "../src/turk/story";
import { CamPath } from "../src/turk/campath";

const W = 1080, H = 1920, FPS = 30;
const MIN_F = Number(process.env.MIN_F ?? 8);   // report cuts held at least this many frames
const sb = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const T = new Timing(sb.scenes.map((s: { duration: number }) => s.duration), sb.captions.words);
const { groups } = buildStory(T);
const cam = new THREE.PerspectiveCamera(40, W / H, 0.05, 200);
const paths = new Map(groups.map((g) => [g, new CamPath(g.cam, g.t0, g.t1)]));
const total = Math.round(T.total * FPS);

type Hit = { key: string; f: number; info: string };
const hits: Hit[] = [];
const right = new THREE.Vector3(), up = new THREE.Vector3(0, 1, 0);

function project(pts: THREE.Vector3[]) {
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, behind = false, minD = Infinity;
  for (const p of pts) {
    const v = p.clone().applyMatrix4(cam.matrixWorldInverse);
    minD = Math.min(minD, -v.z);
    if (v.z > -0.05) { behind = true; continue; }
    const q = p.clone().project(cam);
    const sx = (q.x * 0.5 + 0.5) * W, sy = (0.5 - q.y * 0.5) * H;
    x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy);
  }
  const area = Math.max(1, (x1 - x0) * (y1 - y0));
  const ix = Math.max(0, Math.min(W, x1) - Math.max(0, x0)), iy = Math.max(0, Math.min(H, y1) - Math.max(0, y0));
  return { x0, x1, y0, y1, inside: behind ? 0.5 : (ix * iy) / area, minD, hFrac: (y1 - y0) / H };
}

for (let f = 0; f < total; f++) {
  const t = f / FPS;
  const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6) ?? groups[0];
  const c = paths.get(g)!.at(t);
  cam.fov = c.fov; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
  right.setFromMatrixColumn(cam.matrixWorld, 0); right.y = 0; right.normalize();
  for (const p of g.people) {
    if (p.visible && !p.visible(t)) continue;
    const [x, y, z] = p.at(t);
    const pr = p.props(t) as { seated?: boolean };
    const hgt = (pr.seated ? 1.42 : 1.68) * (p.scale ?? 1), half = 0.3 * (p.scale ?? 1);
    const base = new THREE.Vector3(x, y, z);
    const pts = [-1, 1].flatMap((sx) => [0, hgt].map((h) => base.clone().addScaledVector(right, sx * half).addScaledVector(up, h)));
    const b = project(pts);
    if (b.inside <= 0.02) continue;
    if (b.minD < 1.3 && b.inside < 0.98) hits.push({ key: `${g.id}:${p.id}:near`, f, info: `d ${b.minD.toFixed(2)} in ${b.inside.toFixed(2)}` });
    else if (b.inside < 0.95 && b.hFrac < 1.25) hits.push({ key: `${g.id}:${p.id}:cut`, f, info: `in ${b.inside.toFixed(2)} h ${b.hFrac.toFixed(2)} x ${b.x0.toFixed(0)}..${b.x1.toFixed(0)} y ${b.y0.toFixed(0)}..${b.y1.toFixed(0)}` });
  }
  if (g.cabinet) {
    const [x, y, z] = g.cabinet.at(t);
    const rot = g.cabinet.rotY ?? 0;
    const pts: THREE.Vector3[] = [];
    for (const px of [-0.62, 0.62]) for (const py of [0, 1.9]) for (const pz of [-0.4, 0.4])
      pts.push(new THREE.Vector3(px, py, pz).applyAxisAngle(up, rot).add(new THREE.Vector3(x, y, z)));
    const b = project(pts);
    if (b.inside > 0.02 && b.inside < 0.9 && b.hFrac < 0.9) hits.push({ key: `${g.id}:cabinet:cut`, f, info: `in ${b.inside.toFixed(2)} h ${b.hFrac.toFixed(2)}` });
  }
}

// ranges per key
const by = new Map<string, Hit[]>();
for (const h of hits) { if (!by.has(h.key)) by.set(h.key, []); by.get(h.key)!.push(h); }
for (const [k, hs] of by) {
  const rs: string[] = [];
  let s = hs[0], prev = hs[0];
  for (const h of [...hs.slice(1), null]) {
    if (!h || h.f !== prev.f + 1) { if (prev.f - s.f >= MIN_F) rs.push(`${(s.f / FPS).toFixed(2)}-${(prev.f / FPS).toFixed(2)}s [${s.info}]`); if (h) s = h; }
    if (h) prev = h;
  }
  if (rs.length) console.log(`${k}: ${rs.join("; ")}`);
}
console.log(`groups: ${groups.map((g) => `${g.id} ${g.t0.toFixed(2)}-${g.t1.toFixed(2)}`).join(" | ")}`);
