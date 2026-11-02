// Framing check for the 3D story (our own code): replays every frame's camera from story.ts (pure math, no render)
// and reports figures cut by the frame edge, figures looming in front of the lens and (Turk) the cabinet cut by the edge. Run: node scripts/framing.mjs <storyboard.json> (bundled with esbuild).
import fs from "fs";
import * as THREE from "three";
import { Timing } from "../src/kit/timing";
import { buildStory as turkStory } from "../src/turk/story";
import { buildStory as vasaStory } from "../src/vasa/story";
import { CamPath } from "../src/kit/campath";
import { personBox } from "../src/kit/framing";
import { captionCues, CAP_SIZE, CAP_W } from "../src/kit/Episode3D";
import { parseStoryboard, sceneTimings } from "../../../studio/src/core/schema";
import { paginate } from "../../../studio/src/core/captions";

const W = 1080, H = 1920, FPS = 30;
const MIN_F = Number(process.env.MIN_F ?? 8);   // report cuts held at least this many frames
const sb = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const T = new Timing(sb.scenes.map((s: { duration: number }) => s.duration), sb.captions.words);
// which episode: the storyboard's id (story-chess-turk | story-vasa)
const groups = (sb.id === "story-vasa" ? vasaStory(T).groups : turkStory(T).groups) as (ReturnType<typeof turkStory>["groups"][number] & { avoid?: unknown })[];
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

// caption gate (story-vasa v15; the v14 panel named captions over the rigging, the gun-port row and legs): for every
// caption page, the share of its band that lies over a face or over a group's busy bands, worst
// sampled frame. Pages over CAP_MAX are listed and the script exits 1.
{
  const CAP_MAX = Number(process.env.CAP_MAX ?? 0.12);
  const psb = parseStoryboard(sb);
  const cuts = sceneTimings(psb).timings.slice(1).map((tm) => tm.start / FPS);
  const caps = psb.captions!;
  const words = caps.words.map((w, i) => (i === 0 && w.start < 0.4 ? { ...w, start: 0 } : w));
  const pages = paginate(words, caps, cuts);
  const cues = captionCues(groups, pages, FPS, caps.style.y ?? 0.72);
  const bad: string[] = [];
  pages.forEach((p, i) => {
    const y = cues[i].y;
    // text width calibrated on a rendered v15 frame ("THIRTY SAILORS RAN" is about 675 px: 0.51 x CAP_SIZE per
    // character; 0.56 here to stay on the safe side). captionCues keeps its wider 0.76 for placement.
    const glyphs = p.words.reduce((n, w) => n + w.text.length, 0) * 0.56 + (p.words.length - 1) * 0.3;
    const lines = Math.ceil((glyphs * CAP_SIZE) / CAP_W);
    const half = Math.min(CAP_W, glyphs * CAP_SIZE) / 2, bandH = lines * CAP_SIZE * 0.55;
    const cx = W / 2, top = y * H - bandH, bot = y * H + bandH, area = 4 * half * bandH;
    let worst = 0, at = p.start;
    for (let t = p.start; t < p.end; t += 2 / FPS) {
      // frames inside a whip are smeared (blur up to 16 px): nothing under the caption reads there, so skip them
      if (groups.some((q, qi) => qi > 0 && q.xfade > 0 && Math.abs(t - q.t0) < q.xfade / 2)) continue;
      const g = [...groups].reverse().find((q) => t >= q.t0 - 1e-6) ?? groups[0];
      const c = paths.get(g)!.at(t);
      cam.fov = c.fov; cam.position.copy(c.pos); cam.lookAt(c.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      // busy bands and faces (the top quarter of each figure); legs and subject boxes are allowed under a caption
      const boxes = [...(g.busy ? g.busy(t, [c.pos.x, c.pos.y, c.pos.z]) : []),
        ...g.people.filter((q) => !q.visible || q.visible(t)).map((q) => { const b = personBox(q.at(t), (q.props(t) as { seated?: boolean }).seated === true); return [b[0], b[4] - 0.3 * (b[4] - b[1]), b[2], b[3], b[4], b[5]]; })];
      // union area by rasterising the band on a coarse grid (boxes overlap each other)
      // boxes partly behind the lens are skipped (their screen rectangle is unbounded), as in captionCues
      const rs = boxes.map((b) => { const pts: THREE.Vector3[] = []; for (const x of [b[0], b[3]]) for (const yy of [b[1], b[4]]) for (const z of [b[2], b[5]]) pts.push(new THREE.Vector3(x, yy, z)); return project(pts); })
        .filter((r) => r.inside > 0 && r.inside !== 0.5 && Number.isFinite(r.x0));
      let hit = 0, n = 0;
      for (let gx = cx - half; gx < cx + half; gx += 12) for (let gy = top; gy < bot; gy += 8) { n++; if (rs.some((r) => gx >= r.x0 && gx <= r.x1 && gy >= r.y0 && gy <= r.y1)) hit++; }
      const share = n ? hit / n : 0;
      if (share > worst) { worst = share; at = t; }
    }
    if (worst > CAP_MAX) bad.push(`${p.start.toFixed(2)}s "${p.words.map((w) => w.text).join(" ")}" y ${y} over ${(100 * worst).toFixed(0)}% at ${at.toFixed(2)}s`);
  });
  console.log(`caption gate (band over faces or busy bands > ${(100 * CAP_MAX).toFixed(0)}%): ${bad.length ? "\n  " + bad.join("\n  ") : "clean"}`);
  if (bad.length) process.exitCode = 1;
}
