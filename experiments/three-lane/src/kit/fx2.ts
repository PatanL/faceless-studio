// Effects vocabulary (our own code; RICKSCLIPS_RULEBOOK E1, E4, E6, E8, gap 4). Every effect is a deterministic
// function of story time, lives on the NOINK layer (the world ink pass never outlines it; drawn effects carry their
// own ink), and comes as a Rig factory, so a story file adds it with `rigs: [glints([...]), burst({...})]` and cues it
// on a caption word (acting.wordT). Nothing here shakes the camera (E3: impacts use a hold, a flash or particles).
//   glints   4-point star on the named object: grows 2 f, holds, shrinks 2 f (life 3-12 f, default 8)
//   burst    impact ring + spark stars flying out (8-12 f)
//   debris   15-100 flat inked pieces (shards, coins, paper, splinters) thrown with gravity, one bounce, spin
//   counter  a rolling odometer / gauge texture in the world (digits roll, eased; turns red past `warnAt`)
//   scanPanel + scan   an "outside" picture replaced by an "inside" picture behind a moving bright scan line (5-11 f)
import * as THREE from "three";
import { NOINK } from "../ink";
import { rng } from "../paint";
import type { Rig, V3 } from "./Stage";

const FPS = 30;
const frames = (t: number, t0: number) => Math.floor((t - t0) * FPS + 1e-6);
const canvasTex = (w: number, h: number, draw: (g: CanvasRenderingContext2D) => void) => {
  const c = document.createElement("canvas"); c.width = w; c.height = h;
  draw(c.getContext("2d")!);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
};
const sprite = (map: THREE.Texture, additive = false) => {
  const s = new THREE.Sprite(new THREE.SpriteMaterial({ map, depthTest: false, depthWrite: false, fog: false, transparent: true, toneMapped: false,
    blending: additive ? THREE.AdditiveBlending : THREE.NormalBlending }));
  s.layers.set(NOINK); s.renderOrder = 20; s.visible = false; return s;
};
type At = V3 | ((t: number) => V3);
const posOf = (a: At, t: number): V3 => (typeof a === "function" ? a(t) : a);

// ------------------------------------------------------------------------------------------------ star glint
let starTex: THREE.Texture | null = null;
function star() {
  return (starTex ??= canvasTex(256, 256, (g) => {
    const c = 128;
    const spike = (len: number, w: number, a: number) => {
      g.save(); g.translate(c, c); g.rotate(a);
      g.beginPath(); g.moveTo(0, -len); g.quadraticCurveTo(w * 0.25, -w * 0.25, w, 0); g.quadraticCurveTo(w * 0.25, w * 0.25, 0, len);
      g.quadraticCurveTo(-w * 0.25, w * 0.25, -w, 0); g.quadraticCurveTo(-w * 0.25, -w * 0.25, 0, -len); g.fill(); g.restore();
    };
    const grd = g.createRadialGradient(c, c, 0, c, c, 120);
    grd.addColorStop(0, "rgba(255, 246, 214, 0.55)"); grd.addColorStop(1, "rgba(255, 246, 214, 0)");
    g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
    g.fillStyle = "#fffaf0"; spike(122, 26, 0);
    g.fillStyle = "#fffaf0"; spike(70, 16, Math.PI / 4);
  }));
}
export type GlintCue = { at: At; t: number; size?: number; life?: number };
/** star glints (E1). size in metres (on-screen size follows distance); life in frames (3-12, default 8) */
export const glints = (cues: GlintCue[]): Rig => (ctx) => {
  const ss = cues.map(() => { const s = sprite(star(), true); ctx.root.add(s); return s; });
  return (t) => cues.forEach((c, i) => {
    const s = ss[i], fr = frames(t, c.t), life = Math.max(3, Math.min(12, c.life ?? 8));
    s.visible = fr >= 0 && fr < life;
    if (!s.visible) return;
    // grows over 2 f, holds, shrinks over 2 f; turns 18 degrees over its life
    const k = fr < 2 ? (fr + 1) / 3 : fr >= life - 2 ? (life - fr) / 3 : 1;
    const sz = (c.size ?? 0.35) * k;
    s.scale.set(sz, sz, 1);
    (s.material as THREE.SpriteMaterial).rotation = (fr / life) * 0.32;
    s.position.set(...posOf(c.at, t));
  });
};

// ------------------------------------------------------------------------------------------------ impact burst
let ringTex: THREE.Texture | null = null, sparkTex: THREE.Texture | null = null;
const ring = () => (ringTex ??= canvasTex(256, 256, (g) => { g.lineWidth = 20; g.strokeStyle = "#1b1240"; g.beginPath(); g.arc(128, 128, 104, 0, Math.PI * 2); g.stroke(); g.lineWidth = 10; g.strokeStyle = "#fff4cf"; g.stroke(); }));
const spark = () => (sparkTex ??= canvasTex(64, 64, (g) => {
  g.fillStyle = "#1b1240"; g.beginPath(); g.moveTo(32, 0); g.lineTo(44, 32); g.lineTo(32, 64); g.lineTo(20, 32); g.closePath(); g.fill();
  g.fillStyle = "#ffe08a"; g.beginPath(); g.moveTo(32, 8); g.lineTo(40, 32); g.lineTo(32, 56); g.lineTo(24, 32); g.closePath(); g.fill();
}));
export type BurstCue = { at: At; t: number; size?: number; n?: number; frames?: number; seed?: number };
/** impact ring + spark stars (E4); size = final ring diameter in metres */
export const burst = (cues: BurstCue[]): Rig => (ctx) => {
  const parts = cues.map((c) => {
    const r = rng(c.seed ?? 7);
    const ringS = sprite(ring()); ctx.root.add(ringS);
    const sparks = Array.from({ length: c.n ?? 12 }, () => { const s = sprite(spark()); ctx.root.add(s); return { s, a: r() * Math.PI * 2, v: 0.6 + r() * 0.6, k: 0.6 + r() * 0.5 }; });
    return { ringS, sparks };
  });
  const right = new THREE.Vector3(), up = new THREE.Vector3();
  return (t, cam) => cues.forEach((c, i) => {
    const { ringS, sparks } = parts[i];
    const fr = frames(t, c.t), life = c.frames ?? 10, sz = c.size ?? 1.0;
    const on = fr >= 0 && fr < life, u = (fr + 1) / life;
    const p = new THREE.Vector3(...posOf(c.at, t));
    ringS.visible = on && fr < life - 2;
    if (ringS.visible) { const d = sz * (0.25 + 0.75 * Math.sqrt(u)); ringS.scale.set(d, d, 1); ringS.position.copy(p); (ringS.material as THREE.SpriteMaterial).opacity = 1; }
    right.setFromMatrixColumn(cam.matrixWorld, 0); up.setFromMatrixColumn(cam.matrixWorld, 1);
    for (const sp of sparks) {
      sp.s.visible = on;
      if (!on) continue;
      const d = sz * 0.75 * sp.v * Math.sqrt(u);
      sp.s.position.copy(p).addScaledVector(right, Math.cos(sp.a) * d).addScaledVector(up, Math.sin(sp.a) * d);
      const s = sz * 0.16 * sp.k * (1 - u * 0.8);
      sp.s.scale.set(s * 0.6, s * 1.4, 1);
      (sp.s.material as THREE.SpriteMaterial).rotation = sp.a - Math.PI / 2;
    }
  });
};

// ------------------------------------------------------------------------------------------------ debris
const pieceTex: Record<string, THREE.Texture> = {};
function piece(kind: string) {
  if (pieceTex[kind]) return pieceTex[kind];
  return (pieceTex[kind] = canvasTex(128, 128, (g) => {
    g.lineJoin = "round"; g.lineWidth = 9; g.strokeStyle = "#1b1240";
    if (kind === "coin") { g.fillStyle = "#f2c75a"; g.beginPath(); g.arc(64, 64, 48, 0, Math.PI * 2); g.fill(); g.stroke(); g.fillStyle = "#d9a43a"; g.beginPath(); g.arc(64, 64, 26, 0, Math.PI * 2); g.fill(); }
    else if (kind === "paper") { g.fillStyle = "#f4ecd8"; g.fillRect(20, 14, 88, 100); g.strokeRect(20, 14, 88, 100); g.fillStyle = "#b9ad94"; for (let k = 0; k < 4; k++) g.fillRect(32, 32 + k * 18, 64, 6); }
    else if (kind === "splinter") { g.fillStyle = "#c48a4e"; g.beginPath(); g.moveTo(10, 70); g.lineTo(118, 50); g.lineTo(112, 70); g.lineTo(16, 84); g.closePath(); g.fill(); g.stroke(); }
    else { g.fillStyle = "#cfe6ee"; g.beginPath(); g.moveTo(64, 8); g.lineTo(116, 74); g.lineTo(48, 120); g.lineTo(14, 52); g.closePath(); g.fill(); g.stroke(); }     // shard
  }));
}
export type DebrisCue = { at: At; t: number; n?: number; kind?: "shard" | "coin" | "paper" | "splinter"; size?: number; speed?: number; floorY?: number; life?: number; seed?: number; up?: number };
/** thrown pieces (E4): ballistic with gravity 9.8 m/s^2, one damped bounce on floorY, spin; on the frames grid */
export const debris = (cues: DebrisCue[]): Rig => (ctx) => {
  const sets = cues.map((c) => {
    const r = rng(c.seed ?? 11);
    const mat = new THREE.MeshBasicMaterial({ map: piece(c.kind ?? "shard"), alphaTest: 0.5, side: THREE.DoubleSide, fog: false, toneMapped: true });
    return Array.from({ length: Math.max(15, Math.min(100, c.n ?? 30)) }, () => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), mat); m.layers.set(NOINK); m.visible = false; m.renderOrder = 15; ctx.root.add(m);
      const a = r() * Math.PI * 2, el = 0.35 + r() * 0.9, sp = (c.speed ?? 3) * (0.5 + r() * 0.7);
      return { m, v: new THREE.Vector3(Math.cos(a) * Math.cos(el) * sp, Math.sin(el) * sp * (c.up ?? 1), Math.sin(a) * Math.cos(el) * sp), spin: new THREE.Vector3(r() * 14 - 7, r() * 14 - 7, r() * 14 - 7), s: (c.size ?? 0.12) * (0.6 + r() * 0.8) };
    });
  });
  return (t) => cues.forEach((c, i) => {
    const fr = frames(t, c.t), life = (c.life ?? 1.4) * FPS;
    const p0 = posOf(c.at, c.t), floor = c.floorY ?? 0;
    for (const d of sets[i]) {
      d.m.visible = fr >= 0 && fr < life;
      if (!d.m.visible) continue;
      const s = fr / FPS;
      let y = p0[1] + d.v.y * s - 4.9 * s * s, x = p0[0] + d.v.x * s, z = p0[2] + d.v.z * s;
      // one bounce: time of floor contact, then a damped second arc, then rest
      const disc = d.v.y * d.v.y + 2 * 9.8 * (p0[1] - floor);
      const tHit = (d.v.y + Math.sqrt(Math.max(0, disc))) / 9.8;
      let sp = 1;
      if (s > tHit) {
        const s2 = s - tHit, vy2 = Math.abs(d.v.y - 9.8 * tHit) * 0.35;
        x = p0[0] + d.v.x * (tHit + s2 * 0.4); z = p0[2] + d.v.z * (tHit + s2 * 0.4);
        y = Math.max(floor, floor + vy2 * s2 - 4.9 * s2 * s2) + 0.005;
        sp = Math.max(0, 1 - s2 * 3);
      }
      d.m.position.set(x, y, z);
      d.m.rotation.set(d.spin.x * s * sp, d.spin.y * s * sp, d.spin.z * s * sp);
      d.m.scale.setScalar(d.s);
    }
  });
};

// ------------------------------------------------------------------------------------------------ rolling counter
export type CounterOpts = {
  at: V3; rotY?: number; w?: number; digits?: number; from: number; to: number; t0: number; t1: number;
  label?: string; unit?: string; warnAt?: number; steps?: [number, number][];     // steps: [[t, value]] instead of from/to
};
/** a rolling odometer plate in the world (E6). Each digit column rolls toward the next digit, eased; the plate goes
 * red past warnAt. Its frame is a mesh, so the world ink outlines it. Redraws only when the shown value changes. */
export const counter = (o: CounterOpts): Rig => (ctx) => {
  const n = o.digits ?? 4, W = 128 * n + 80, H = 300;
  const c = document.createElement("canvas"); c.width = W; c.height = H;
  const g = c.getContext("2d")!;
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 4;
  const w = o.w ?? 1.2, h = (w * H) / W;
  const plate = new THREE.Mesh(new THREE.BoxGeometry(w + 0.06, h + 0.06, 0.05), new THREE.MeshLambertMaterial({ color: "#2b2440" }));
  const face = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: tex, fog: false, toneMapped: true }));
  face.position.z = 0.03; face.layers.set(NOINK);
  const grp = new THREE.Group(); grp.add(plate, face); grp.position.set(...o.at); grp.rotation.y = o.rotY ?? 0; ctx.root.add(grp);
  const ease = (u: number) => { u = Math.min(1, Math.max(0, u)); return u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
  const valueAt = (t: number) => {
    if (o.steps) { let v = o.steps[0][1]; for (let i = 1; i < o.steps.length; i++) { const [ti, vi] = o.steps[i]; const tp = o.steps[i - 1][0]; if (t >= ti) v = vi; else if (t > tp && t > ti - 0.3) v = v + (vi - v) * ease((t - (ti - 0.3)) / 0.3); } return v; }
    return o.from + (o.to - o.from) * ease((t - o.t0) / Math.max(1e-3, o.t1 - o.t0));
  };
  let last = "";
  const draw = (v: number) => {
    const warn = o.warnAt !== undefined && v >= o.warnAt;
    g.fillStyle = warn ? "#5a1624" : "#1d1a33"; g.fillRect(0, 0, W, H);
    g.fillStyle = "#f2e6c8"; g.font = '700 46px "Montserrat", Arial, sans-serif'; g.textAlign = "center"; g.textBaseline = "middle";
    if (o.label) g.fillText(o.label, W / 2, 40);
    for (let i = 0; i < n; i++) {
      const place = Math.pow(10, n - 1 - i);
      const raw = v / place;                        // this column rolls with the fraction of the column below it
      const d = Math.floor(raw) % 10, frac = place === 1 ? raw - Math.floor(raw) : Math.max(0, (v % place) / place - 0.9) * 10;
      const x = 40 + i * 128;
      g.fillStyle = "#f7f1e2"; g.fillRect(x + 6, 84, 116, 180);
      g.save(); g.beginPath(); g.rect(x + 6, 84, 116, 180); g.clip();
      g.fillStyle = warn ? "#c22a2a" : "#1b1240"; g.font = '900 150px "Montserrat", Arial, sans-serif';
      g.fillText(String(d), x + 64, 180 - frac * 180); g.fillText(String((d + 1) % 10), x + 64, 360 - frac * 180);
      g.restore();
      g.strokeStyle = "#1b1240"; g.lineWidth = 8; g.strokeRect(x + 6, 84, 116, 180);
    }
    if (o.unit) { g.fillStyle = "#f2e6c8"; g.font = '700 34px "Montserrat", Arial, sans-serif'; g.fillText(o.unit, W / 2, 286); }
    tex.needsUpdate = true;
  };
  return (t) => { const v = valueAt(t); const k = v.toFixed(2); if (k !== last) { last = k; draw(v); } };
};

// ------------------------------------------------------------------------------------------------ scan-line reveal
/** a panel showing `outside`, replaced by `inside` above/below a bright scan line at uLine (0..1, top to bottom) */
export function scanPanel(outside: THREE.Texture, inside: THREE.Texture, w: number, h: number) {
  const uni = { uIn: { value: inside }, uLine: { value: -0.1 }, uDir: { value: 1 } };
  const mat = new THREE.MeshBasicMaterial({ map: outside, fog: false });
  mat.onBeforeCompile = (sh: { uniforms: Record<string, unknown>; fragmentShader: string }) => {
    Object.assign(sh.uniforms, uni);
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", "#include <common>\nuniform sampler2D uIn; uniform float uLine; uniform float uDir;")
      .replace("#include <map_fragment>", [
        "#include <map_fragment>",
        "float yy = 1.0 - vMapUv.y;",                                        // 0 at the top edge
        "float past = uDir > 0.0 ? step( yy, uLine ) : step( uLine, yy );",  // the part the line has already swept
        "vec4 inC = texture2D( uIn, vMapUv );",
        "diffuseColor.rgb = mix( diffuseColor.rgb, inC.rgb, past );",
        "float band = smoothstep( 0.03, 0.0, abs( yy - uLine ) );",
        "diffuseColor.rgb += vec3( 0.55, 0.95, 1.0 ) * band * 1.4;",
      ].join("\n"));
  };
  mat.customProgramCacheKey = () => "nextScan1";
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat);
  mesh.layers.set(NOINK);
  return { mesh, uni };
}
/** drive a scanPanel: the line sweeps down (dir 1) or up (-1) over `frames` (5-11 per E8), on 1s */
export const scan = (panel: ReturnType<typeof scanPanel>, t0: number, nFrames = 9, dir: 1 | -1 = 1): Rig => () => (t) => {
  const fr = frames(t, t0);
  const u = Math.min(1.1, Math.max(-0.1, (fr + 1) / nFrames));
  panel.uni.uDir.value = dir;
  panel.uni.uLine.value = fr < 0 ? (dir > 0 ? -0.1 : 1.1) : dir > 0 ? u : 1 - u;
};

// ---------------------------------------------------------------- drop a prop on a word (round 3, replication lesson 8)
/** a gravity fall from `from` to `to` between t0 and t1 (seconds): before t0 it rests at `from`; after t1 at `to`, or
 * gone with `vanish` (a ball swallowed by a frog). Horizontal motion is linear, vertical accelerates. */
export const fall = (from: V3, to: V3, t0: number, t1: number, vanish = false) => (t: number): V3 | null => {
  if (t >= t1) return vanish ? null : to;
  if (t < t0) return from;
  const u = (t - t0) / (t1 - t0);
  return [from[0] + (to[0] - from[0]) * u, from[1] + (to[1] - from[1]) * u * u, from[2] + (to[2] - from[2]) * u];
};
export type DropCue = { make: () => THREE.Object3D; from: V3; to: V3; t: number; dur?: number; vanish?: boolean; impact?: number; visibleFrom?: number };
/** drop props on words: each cue falls from `from` onto `to` starting at its word time t (dur s, default 10 f), with an
 * impact burst on landing (impact = burst size, 0 = none) */
export const drop = (cues: DropCue[]): Rig => (ctx) => {
  const objs = cues.map((c) => { const o = c.make(); ctx.root.add(o); return o; });
  const hits = burst(cues.filter((c) => (c.impact ?? 0.4) > 0).map((c) => ({ at: c.to, t: c.t + (c.dur ?? 1 / 3), size: c.impact ?? 0.4 })))(ctx);
  return (t, cam) => {
    cues.forEach((c, i) => { const p = fall(c.from, c.to, c.t, c.t + (c.dur ?? 1 / 3), c.vanish)(t); const o = objs[i]; o.visible = !!p && (c.visibleFrom === undefined || t >= c.visibleFrom); if (p) o.position.set(...p); });
    hits(t, cam);
  };
};
