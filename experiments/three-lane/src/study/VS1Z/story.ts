// REPLICATION STUDY (internal, never published): the first 20 s (F0-F599) of the reference VS1Z, shot for shot, on our
// own kit and characters. Every number below is a reference frame (30 fps) read off the every-frame sheets; the camera
// uses the kit's exact path mode (CamKey.ease), so each key is a measured framing at a measured frame. The notes per
// shot are in out/study/VS1Z/DECODE.md.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../../kit/Stage";
import type { CamKey, Ease } from "../../kit/campath";
import type { Timing } from "../../kit/timing";
import { glints, burst, fall as kitFall } from "../../kit/fx2";
import { frameKey as kitFrameKey } from "../../kit/framing";
import { bokeh } from "../../kit/depth";
import { glaze, metal } from "../../kit/materials";
import { depthPlate } from "../../kit/plate";
import { makeKey } from "../../kit/sets";
import { NOINK } from "../../ink";
import { orb } from "../../kit/heroprops";
import { candelabra } from "../../kit/interior";
import { walkers, shifters, birds, smokeColumns, flagsRig } from "../../kit/worldbuild";
import { PRESETS, type Preset } from "../../kit/presets";
import { hallSet, balconySet, flamesRig, ballRig, mouthOf, frogMouthOf, headOf, JAR, EMPEROR, GUARDS, THRONE_Z, BAL_EMP } from "./sets";

export type StudyStory = { groups: GroupSpec[] };
const F = (f: number) => f / 30;

/** frameKey with reference frame numbers (the kit's framing.ts frameKey takes seconds) */
const frameKey = (f: number, S: V3, sx: number, sy: number, h: number, frac: number, az: number, el: number, fov = 40, ease?: Ease, curve?: boolean): CamKey => kitFrameKey(F(f), S, sx, sy, h, frac, az, el, fov, ease ?? "lin", curve);
/** a lens move from a fixed spot: aim so world point T lands at screen (sx, sy) with this fov */
const aimKey = (f: number, pos: V3, T: V3, sx: number, sy: number, fov: number, ease: Ease = "lin"): CamKey => {
  const P = new THREE.Vector3(...pos), d0 = new THREE.Vector3(...T).sub(P), dist = d0.length(); d0.normalize();
  const th = Math.tan((fov * Math.PI) / 360), pitch = Math.atan((sy - 0.5) * 2 * th), yaw = Math.atan((sx - 0.5) * 2 * th * (9 / 16));
  const right = new THREE.Vector3().crossVectors(d0, new THREE.Vector3(0, 1, 0)).normalize(), up = new THREE.Vector3().crossVectors(right, d0);
  const dir = d0.clone().applyAxisAngle(right, pitch).applyAxisAngle(up, yaw);
  return { t: F(f), pos, look: P.clone().addScaledVector(dir, dist).toArray() as V3, fov, ease };
};
const K = (f: number, pos: V3, look: V3, fov = 40, ease: Ease = "lin", curve = false): CamKey => ({ t: F(f), pos, look, fov, ease, curve });
/** a step track from [frame, value] pairs */
const steps = <T,>(keys: [number, T][]) => keys.map(([f, v]) => ({ t: F(f), v }));

const HEAD_Y = 1.375, HEAD_H = 0.59;                       // Actor: head centre above the feet, head height (scale 1)
const head = (p: V3, s = 1): V3 => [p[0], p[1] + HEAD_Y * s, p[2]];

const HALL: Preset = { ...PRESETS.candle };   // round 3: the kit's candle-lit interior (was golden with a violet shade)
const DAY: Preset = { ...PRESETS.day, fogNear: 60, fogFar: 420 };

/** the inventor's arm as a stick reaching into the dragon's mouth with the ball, then withdrawn (the hook close-up) */
const armRig = (from: V3, to: V3, f0: number, fOut0: number, fOut1: number): Rig => (ctx) => {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 1, 8), new THREE.MeshLambertMaterial({ color: "#1b1720" }));
  const hand = new THREE.Mesh(new THREE.SphereGeometry(0.06, 10, 8), m.material); ctx.root.add(m, hand);
  const A = new THREE.Vector3(...from), B = new THREE.Vector3(...to);
  return (t) => {
    const fr = t * 30, vis = fr >= f0 && fr < fOut1;
    m.visible = hand.visible = vis; if (!vis) return;
    const u = Math.min(1, Math.max(0, (fr - fOut0) / (fOut1 - fOut0)));
    const tip = B.clone().lerp(A, u * u * 1.4).add(new THREE.Vector3(-0.08, -0.06, 0.02));
    const mid = A.clone().add(tip).multiplyScalar(0.5), len = A.distanceTo(tip);
    m.position.copy(mid); m.scale.set(1, len, 1); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tip.clone().sub(A).normalize());
    hand.position.copy(tip);
  };
};
/** a ball falling from a dragon mouth into its frog (the kit's drop path, gravity, landing at f1, swallowed) */
const fall = (i: number, f0: number, f1: number) => kitFall(mouthOf(i), frogMouthOf(i), F(f0), F(f1), true);
/** bokeh discs on the hall's candles and fire bowls (round 3, kit/depth.ts) */
const hallBokeh = (k = 5): Rig => (ctx) => bokeh((ctx.set as unknown as { lights: V3[] }).lights, { color: "#ffb45c", k })(ctx);
/** shot 5's banquet: a long lacquered table across the hall behind the jar, dishes and candles (round 3) */
const COURT: V3[] = [-3.6, -2.4, -1.2, 1.6, 2.8, 4.0].map((x) => [x, 0, -5.6] as V3);
const banquet = (): Rig => (ctx) => {
  const g = new THREE.Group(); g.position.set(0.2, 0, -4.9); ctx.root.add(g);
  const top = new THREE.Mesh(new THREE.BoxGeometry(9.5, 0.12, 1.1), glaze("#5a1e1a", { rough: 0.35 })); top.position.y = 0.82; g.add(top);
  const cloth = new THREE.Mesh(new THREE.BoxGeometry(9.6, 0.5, 1.12), new THREE.MeshLambertMaterial({ color: "#c49a3a" })); cloth.position.y = 0.6; g.add(cloth);
  for (let k = 0; k < 9; k++) { const d = orb("gold", 0.11); d.scale.set(1.4, 0.35, 1.4); d.position.set(-4.2 + k * 1.05, 0.9, 0.1); g.add(d);
    const fr = orb("bronze", 0.05); fr.position.set(-4.2 + k * 1.05, 0.98, 0.1); g.add(fr); }
  const c = candelabra({ n: 3, h: 0.6, spread: 0.2 }); c.position.set(-1.0, 0.88, 0.2); g.add(c);
  const c2 = candelabra({ n: 3, h: 0.6, spread: 0.2 }); c2.position.set(2.6, 0.88, 0.2); g.add(c2);
  g.traverse((o) => { if ((o as THREE.Mesh).isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return () => {};
};
/** world building (round 3): background life in the hall: servants walking the side aisles and across the back, courtiers
 * shifting their weight either side of the dais (all extras: exempt from cast/edge gates) */
const hallLife = (): PersonSpec[] => [
  ...walkers("servant", [[[-6.4, 0, -1.5], [-6.4, 0, -12.5]], [[6.4, 0, -12.5], [6.4, 0, -2.0]], [[-3.6, 0, -9.8], [3.6, 0, -9.8]]], { costumes: ["courtOfficial2", "scholar", "courtOfficial"], speed: 0.8 }),
  ...shifters("courtier", [[-3.4, 0, -12.2], [-2.6, 0, -11.6], [2.6, 0, -11.6], [3.4, 0, -12.2]], { costumes: ["courtOfficial", "courtOfficial2"], poses: ["stand", "hold", "hips", "stand"], every: 2.6, face: [0, 1, 0] }),
];
const balconyLife = (): Rig[] => [birds({ from: [-80, 30, -90], to: [80, 42, -120], n: 9, size: 1.4, period: 12 }), smokeColumns([[-50, -2, -205], [25, -2, -210], [70, -2, -235]], { scale: 4 }), flagsRig()];
const DBG = (p: V3): Rig => (ctx) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.06), new THREE.MeshBasicMaterial({ color: "#ff0000", depthTest: false })); m.renderOrder = 99; m.position.set(...p); ctx.root.add(m); return () => {}; };
/** a world point at screen (sx, sy) and distance dist from a CamKey's camera (for props framed in a key frame) */
const atScreen = (k: CamKey, sx: number, sy: number, dist: number): V3 => {
  const c = new THREE.PerspectiveCamera(k.fov ?? 40, 9 / 16); c.position.set(...k.pos); c.lookAt(new THREE.Vector3(...k.look)); c.updateMatrixWorld();
  const th = Math.tan(((k.fov ?? 40) * Math.PI) / 360), v = new THREE.Vector3((sx - 0.5) * 2 * th * (9 / 16) * dist, -(sy - 0.5) * 2 * th * dist, -dist).applyMatrix4(c.matrixWorld);
  return [v.x, v.y, v.z];
};
/** the hook's foreground, after the Codex key frame (main path): candles in a gold bowl bottom-left, an incense burner,
 * a low table with scroll rolls and a blue-and-white brush pot bottom-right; world-placed from the F0 camera so the push
 * leaves them behind (a real near layer, blurred by the lens) */
const hookForeground = (k: CamKey): Rig => (ctx) => {
  const gold = metal("gold", { engrave: true, repeat: [2, 1] }), wax = glaze("#f2ead6", { rough: 0.5 }), flameM = new THREE.MeshBasicMaterial({ color: new THREE.Color("#ffd890").multiplyScalar(2.4) });
  const put = (o: THREE.Object3D, sx: number, sy: number, d: number, dy = 0) => { const p = atScreen(k, sx, sy, d); o.position.set(p[0], p[1] + dy, p[2]); o.lookAt(new THREE.Vector3(k.pos[0], o.position.y, k.pos[2])); ctx.root.add(o); return o; };
  const candles = new THREE.Group();
  const bowl = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.3, 0.02], [0.36, 0.14], [0.34, 0.16], [0, 0.16]].map(([x, y]) => new THREE.Vector2(x, y)), 32), gold); candles.add(bowl);
  for (const [x, z, h] of [[-0.12, 0.02, 0.32], [0.1, -0.05, 0.24], [0.02, 0.12, 0.18]]) { const c = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, h, 16), wax); c.position.set(x, 0.16 + h / 2, z); candles.add(c);
    const f = new THREE.Mesh(new THREE.SphereGeometry(0.03, 10, 8), flameM); f.scale.set(1, 2, 1); f.position.set(x, 0.16 + h + 0.05, z); f.layers.set(NOINK); f.userData.bloom = true; candles.add(f); }
  put(candles, 0.1, 0.9, 1.5, -0.25);
  const burner = new THREE.Mesh(new THREE.LatheGeometry([[0, 0], [0.12, 0], [0.16, 0.08], [0.2, 0.2], [0.17, 0.3], [0.08, 0.36], [0.1, 0.42], [0.04, 0.5], [0, 0.52]].map(([x, y]) => new THREE.Vector2(x, y)), 32), gold);
  put(burner, 0.36, 0.95, 1.6, -0.3);
  const table = new THREE.Group(); const wood = glaze("#5a2418", { rough: 0.4 });
  const top = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.06, 0.6), wood); top.position.y = 0.3; table.add(top);
  for (const [x, z] of [[-0.5, -0.25], [0.5, -0.25], [-0.5, 0.25], [0.5, 0.25]]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.3, 0.05), wood); l.position.set(x, 0.15, z); table.add(l); }
  for (let i = 0; i < 3; i++) { const sc = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.42, 16), glaze("#efe0bc", { rough: 0.6 })); sc.rotation.z = Math.PI / 2; sc.position.set(-0.25 + i * 0.06, 0.37 + (i === 2 ? 0.08 : 0), -0.1 + i * 0.09); table.add(sc);
    const tie = new THREE.Mesh(new THREE.TorusGeometry(0.047, 0.008, 6, 16), glaze("#b8302f")); tie.rotation.y = Math.PI / 2; tie.position.copy(sc.position); table.add(tie); }
  const pot = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.09, 0.24, 24), glaze("#e8eef8", { rough: 0.25 })); pot.position.set(0.32, 0.45, 0.05); table.add(pot);
  for (let i = 0; i < 4; i++) { const br = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.012, 0.36, 6), glaze("#3a2a1a")); br.position.set(0.3 + i * 0.02, 0.6, 0.05 + (i % 2) * 0.03); br.rotation.z = -0.15 + i * 0.1; table.add(br); }
  put(table, 0.86, 0.93, 1.7, -0.32);
  ctx.root.traverse((o) => { if ((o as THREE.Mesh).isMesh && !(o as THREE.Mesh).castShadow) { o.castShadow = true; o.receiveShadow = true; } });
  return () => {};
};

/** round 3 pilot, technique 1 (trial): the hook push-in as a key frame + depth plate. The key camera sits at KEYCAM; the
 * plate (public/kf/hook_*) is the Codex key frame displaced by Depth Anything V2; our live inventor card stands on the
 * painted one (feet at screen (0.22, 0.79), 3.4 m); the push is a lens push (zoom) with a 0.1 m dolly, within the
 * plate's measured limits */
const KEYCAM: CamKey = { t: 0, pos: [0, 1.6, 10], look: [0, 1.6, 0], fov: 40 };
function plateHook(groups: GroupSpec[], invFace: { t: number; v: string }[]) {
  const dragon = atScreen(KEYCAM, 0.62, 0.42, 4.06), feet = atScreen(KEYCAM, 0.22, 0.79, 3.4);
  const fwd = (d: number): V3 => [0, 1.6, 10 - d];
  groups[0] = { ...groups[0], set: () => { const root = new THREE.Group(); return { root, key: makeKey(root, [-6, 9, 14], [0, 1, 5], 12), glows: [], extra: {} }; }, light: HALL, lens: { cInf: 0.01 },
    cam: [{ ...KEYCAM, ease: "lin" }, { t: F(20), pos: fwd(0.04), look: [0.02, 1.6, 0], fov: 39.4, ease: "lin" },
      aimKey(33, fwd(0.1), dragon, 0.45, 0.4, 15.5, "io"), aimKey(58, fwd(0.12), dragon, 0.45, 0.4, 14.5, "lin"), aimKey(92, fwd(0.12), dragon, 0.45, 0.4, 14.5, "lin")],
    people: [{ id: "inventor", scale: 0.62, at: () => feet, faceTo: () => dragon, props: () => ({ costume: "scholar", seed: 1, face: invFace, pose: steps([[0, "holdHigh"]]), blinks: [] }) }],
    rigs: [depthPlate("hook", KEYCAM)], alive: [[0, F(92)]] };
}
export function buildStudy(_T: Timing, o: { plate?: boolean } = {}): StudyStory {
  const groups: GroupSpec[] = [];
  const INV: V3 = [-1.45, 0, 1.25];
  const INV2: V3 = [-0.55, 0, 2.55];
  const emperorSpec = (face: { t: number; v: string }[], pose: { t: number; v: string }[] = steps([[0, "stand"]])): PersonSpec =>
    ({ id: "emperor", scale: 1.05, at: () => EMPEROR, props: () => ({ costume: "hanEmperor", seed: 3, face, pose, blinks: [] }) });
  const guardSpecs = (face: { t: number; v: string }[], pose: { t: number; v: string }[] = steps([[0, "stand"]])): PersonSpec[] =>
    GUARDS.map((g, k) => ({ id: `guard${k}`, at: () => g, faceTo: () => EMPEROR, props: () => ({ costume: "hanGuard", seed: 7 + k, face, pose, blinks: [] }) }));
  const JC: V3 = [JAR[0], 1.5, JAR[2]];

  // ===== shot 1, F0-F91 (one camera move): the inventor at the jar (smug), push into the dragon's mouth as the arm
  // leaves the ball, glint on "mouth", crane up over the jar lid to the emperor on his dais
  {
    const invFace = steps([[0, "smug"], [14, "stunned"]]);
    groups.push({
      id: "hook", place: "hall", t0: 0, t1: F(92), xfade: 0, set: hallSet, env: "candle", light: HALL, lens: { cInf: 11 },
      cam: [
        frameKey(0, head(INV), 0.33, 0.47, HEAD_H, 0.19, 10, 4),
        frameKey(20, head(INV), 0.335, 0.47, HEAD_H, 0.2, 10, 4, 40, "lin"),
        frameKey(33, headOf(0), 0.55, 0.4, 0.6, 0.5, 34, 6, 40, "io"),
        frameKey(58, headOf(0), 0.55, 0.4, 0.6, 0.55, 34, 6, 40, "lin"),
        K(66, [0.0, 2.75, 2.2], [0.2, 2.7, -8], 34, "in", true),
        K(72, [0.4, 3.85, 1.45], [0.05, 1.75, THRONE_Z], 27, "out", true),
        K(91, [0.4, 3.83, 1.2], [0.05, 1.75, THRONE_Z], 26, "lin"),
      ],
      people: [
        { id: "inventor", at: () => INV, faceTo: () => headOf(0), props: () => ({ costume: "scholar", seed: 1, face: invFace, pose: steps([[0, "holdHigh"]]), blinks: [] }) },
        emperorSpec(steps([[0, "frown"]])), ...guardSpecs(steps([[0, "frown"]])),
      ],
      rigs: [flamesRig(), hallBokeh(), ballRig((i) => mouthOf(i)), armRig([-1.15, 1.15, 1.35], mouthOf(0), 21, 36, 43), hookForeground(frameKey(0, head(INV), 0.33, 0.47, HEAD_H, 0.19, 10, 4)),
        glints([{ at: mouthOf(0), t: F(52), size: 0.16, life: 8 }])],
      alive: [[0, F(92)]],
    });
  }
  // ===== shot 2, F92-F223 (the only hard cut, then one camera): the inventor's warning; the ball drops on "falls";
  // sweat and ring eyes on "out,"/"run.", a snap punch-in with speed lines on "run.", then the camera travels past the
  // jar down the aisle to the emperor's frown, which turns into a laugh on "burst"; pull back to the laughing court
  {
    const invFace = steps([[92, "focus"], [101, "sly"], [109, "stunned"], [117, "focus"], [120, "angry"], [125, "focus"], [131, "stunned"], [136, "terrified"], [144, "stunned"]]);
    const invPose = steps([[92, "hold"], [120, "point"], [130, "hold"], [143, "strikeUp"]]);
    const empH = head(EMPEROR, 1.05);
    groups.push({
      id: "warning", place: "hall", t0: F(92), t1: F(225), xfade: 0, join: { kind: "cut" }, cropOK: ["guard0", "guard1"],   // the master crops the flanking guards on purpose (F168-F192)
      set: hallSet, env: "candle", light: HALL, lens: { cInf: 10 },
      cam: [
        frameKey(92, head(INV), 0.36, 0.47, HEAD_H, 0.19, 4, 3),
        frameKey(142, head(INV), 0.37, 0.47, HEAD_H, 0.2, 4, 3, 40, "lin"),
        frameKey(150, head(INV), 0.55, 0.56, HEAD_H, 0.222, 0, 3, 40, "snap"),
        frameKey(158, head(INV), 0.58, 0.58, HEAD_H, 0.23, -2, 3, 40, "lin"),
        { ...K(161, [-2.2, 2.0, 2.6], [1.5, 1.7, -5], 40, "in", true), soft: 5 },
        { ...K(166, [-1.9, 2.1, -3.0], [0, 1.95, THRONE_Z], 40, "io", true), soft: 5 },   // the fly-past past the jar: smoothed wider (round 3)
        frameKey(170, empH, 0.48, 0.38, HEAD_H * 1.05, 0.21, 0, 2, 40, "out", true),
        frameKey(185, empH, 0.48, 0.38, HEAD_H * 1.05, 0.22, 0, 2, 40, "lin"),
        { ...frameKey(200, empH, 0.5, 0.45, HEAD_H * 1.05, 0.07, 0, 7, 55, "io"), soft: 6 },   // round 3: the laugh pull-back eased wider (it stepped 32 px/f^2 against the master's max 30)
        frameKey(225, empH, 0.5, 0.45, HEAD_H * 1.05, 0.075, 0, 7, 55, "lin"),
      ],
      people: [
        { id: "inventor", at: () => INV, faceTo: (t) => (t < F(143) ? headOf(0) : [-4, 2, 0]), props: () => ({ costume: "scholar", seed: 1, face: invFace, pose: invPose, blinks: [F(117)], marks: [{ t0: F(136), kind: "sweat" }] }) },
        emperorSpec(steps([[0, "frown"], [180, "grimace"], [183, "laugh"], [193, "cackle"]]), steps([[0, "stand"], [193, "laugh"]])),
        ...guardSpecs(steps([[0, "frown"], [186, "laugh"], [196, "cackle"]]), steps([[0, "stand"], [190, "laugh"]])),
      ],
      rigs: [flamesRig(), hallBokeh(), ballRig((i, t) => (i === 0 ? fall(0, 121, 131)(t) : mouthOf(i)))],
      alive: [[F(92), F(225)]],
    });
  }
  // ===== shot 3, F225-F404 (4 f dissolve in): the jar from high on the right, orbiting to the front and coming down
  // ("eight dragons coiled around a giant bronze jar"), a push to the front dragon, a tilt down to the frog's mouth
  {
    const k345 = frameKey(352, JC, 0.5, 0.47, 3.4, 0.67, 2, 17, 42, "lin", true);   // the push F300-F345 at the master's 0.57 %/f (was 1.07)   // the jar fills the frame (master F349)
    const orbit = [frameKey(217, JC, 0.5, 0.44, 3.4, 0.42, -40, 21, 44), frameKey(250, JC, 0.5, 0.44, 3.4, 0.43, -22, 20, 44, "lin", true),   // -40: clear of the column; keys set 6-10 f early against the 4 f smoothing   // -38: clear of the column
      frameKey(300, JC, 0.5, 0.45, 3.4, 0.52, -2, 19, 44, "lin", true)];
    groups.push({
      id: "jar", place: "hall", t0: F(225), t1: F(405), xfade: 0, join: { kind: "dissolve", frames: 4 }, set: hallSet, env: "candle", light: HALL, lens: { cInf: 6 },
      cam: [
        // round 3 shot-3 fix (owner: "theirs actually orbits"), measured on the master with camera_motion.py:
        // F225-F300 an orbit (background -2.4..-3.1 px/f at 720, zoom from F260 at 0.6 %/f), F300-F345 a slow push
        // (0.57 %/f), F345-F362 the push to one dragon (1.0 %/f), F362-F404 the tilt down to the frog (-9..-12 px/f)
        ...orbit, k345,
        // the master's push to the dragon and tilt to the frog are lens moves from one spot (uniform zoom 1.0 %/f with a
        // tilt up, then a tilt down of ~0.36 frame with a slight zoom out), not dollies: aimed from the F345 position
        aimKey(368, k345.pos, headOf(1), 0.5, 0.42, 30, "io"),   // tight on the dragon, the frog below frame; a tilt up (content down, as theirs)
        aimKey(410, k345.pos, frogMouthOf(1), 0.5, 0.78, 38, "out"),   // the tilt down to the frog, fast then settling (theirs -12, -9 px/f)
        aimKey(412, k345.pos, frogMouthOf(1), 0.5, 0.78, 38, "lin"),
      ],
      people: [emperorSpec(steps([[0, "frown"]])), ...guardSpecs(steps([[0, "frown"]]))].map((p) => ({ ...p, extra: true })),   // specks far behind the jar, as in the master
      rigs: [flamesRig(), hallBokeh(), ballRig((i) => mouthOf(i))],
      alive: [[F(225), F(405)]],
    });
  }
  // ===== shot 4, F405-F535 (6 f dissolve in): the emperor on his balcony; on "biggest" the camera cranes up over his
  // head to the army filling the parade ground, holds, and comes back down to his frown for "from a jar."
  {
    const H = head(BAL_EMP, 1.05);
    groups.push({
      id: "balcony", place: "balcony", t0: F(405), t1: F(536), xfade: 0, join: { kind: "dissolve", frames: 6 }, set: balconySet, light: DAY, lens: { cInf: 1.5 },
      cam: [
        // round 3: DECODE (corrected, 61a134b): a slow rise and pull-back drifting him to (0.3, 0.45) by F420, then a
        // rising pull-back with a tilt down that keeps him in frame, small at the bottom (head 0.05 at (0.5, 0.93)) over
        // the army, a drift, a crane back down to his frown at (0.55, 0.4)
        frameKey(402, H, 0.55, 0.40, HEAD_H * 1.05, 0.13, -8, 2),
        frameKey(420, H, 0.3, 0.45, HEAD_H * 1.05, 0.115, -8, 6, 40, "lin"),
        frameKey(427, H, 0.32, 0.5, HEAD_H * 1.05, 0.105, -8, 8, 40, "lin"),
        frameKey(445, H, 0.5, 0.92, HEAD_H * 1.05, 0.045, -4, 14, 50, "io5"),   // the master's wide: parade ground, city and mountains, horizon high
        frameKey(497, H, 0.5, 0.91, HEAD_H * 1.05, 0.047, -4, 14, 50, "lin"),
        frameKey(512, H, 0.55, 0.40, HEAD_H * 1.05, 0.13, 5, 2, 40, "io"),
        frameKey(540, H, 0.55, 0.42, HEAD_H * 1.05, 0.135, 5, 2, 40, "lin"),
      ],
      people: [{ id: "emperor", scale: 1.05, at: () => BAL_EMP, props: () => ({ costume: "hanEmperor", seed: 3, face: steps([[0, "frown"], [503, "angry"], [512, "frown"]]), pose: steps([[0, "stand"]]), blinks: [F(470)] }) }],
      alive: [[F(405), F(536)]],
    });
  }
  // ===== shot 5, F536-F599 (5 f dissolve in): weeks later, the inventor dozing at the jar; a ball drops into a frog
  // with an impact burst on "fell,", he jolts awake; the camera starts a fast push to the right
  {
    groups.push({
      id: "later", place: "hall", t0: F(536), t1: F(600), xfade: 0, join: { kind: "dissolve", frames: 5 }, set: hallSet, env: "candle", light: HALL, lens: { cInf: 9 },
      cam: [
        frameKey(534, head(INV2), 0.27, 0.6, HEAD_H, 0.09, -12, 9),
        frameKey(594, head(INV2), 0.3, 0.58, HEAD_H, 0.1, -12, 9, 40, "lin"),
        frameKey(603, head(INV2), 0.05, 0.6, HEAD_H, 0.19, 14, 6, 40, "out"),
      ],
      people: [...COURT.map((p, k) => ({ id: `court${k}`, extra: true, at: () => p, faceTo: () => [0, 1, 6] as V3, props: () => ({ costume: ["courtOfficial", "courtOfficial2"][k % 2], seed: 20 + k, face: ["neutral", "smug", "focus", "sly"][k % 4], pose: "stand", blinks: [] }) })),
        { id: "inventor", at: () => INV2, faceTo: () => headOf(1), props: () => ({ costume: "scholar", seed: 1, face: steps([[0, "sleepy"], [570, "stunned"], [575, "grimace"], [585, "stunned"], [594, "sly"]]), pose: steps([[0, "stand"], [570, "shrug"], [580, "stand"]]), blinks: [] }) }],
      rigs: [flamesRig(), hallBokeh(), banquet(), ballRig((i, t) => (i === 1 ? fall(1, 555, 569)(t) : mouthOf(i))), burst([{ at: frogMouthOf(1), t: F(569), size: 0.9, n: 10 }])],
      alive: [[F(536), F(600)]],
    });
  }
  if (o.plate) plateHook(groups, steps([[0, "smug"], [14, "stunned"]]));
  // round 3 world building: hall groups get the background life, the balcony its birds, smoke and flags
  for (const g of groups) {
    if (g.env === "candle") g.people = [...g.people, ...hallLife()];
    if (g.id === "balcony") g.rigs = [...(g.rigs ?? []), ...balconyLife()];
  }
  return { groups };
}
