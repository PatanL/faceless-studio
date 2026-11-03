// REPLICATION STUDY (internal, never published): the first 20 s (F0-F599) of the reference VS1Z, shot for shot, on our
// own kit and characters. Every number below is a reference frame (30 fps) read off the every-frame sheets; the camera
// uses the kit's exact path mode (CamKey.ease), so each key is a measured framing at a measured frame. The notes per
// shot are in out/study/VS1Z/DECODE.md.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../../kit/Stage";
import type { CamKey, Ease } from "../../kit/campath";
import type { Timing } from "../../kit/timing";
import { glints, burst } from "../../kit/fx2";
import { PRESETS, type Preset } from "../../kit/presets";
import { hallSet, balconySet, flamesRig, ballRig, mouthOf, frogMouthOf, headOf, JAR, EMPEROR, GUARDS, THRONE_Z, BAL_EMP } from "./sets";

export type StudyStory = { groups: GroupSpec[] };
const F = (f: number) => f / 30;
const D2R = Math.PI / 180;
const ASPECT = 9 / 16;

/** a framing: world point S lands at screen (sx, sy) (0..1, y down), a world height h fills `frac` of the frame height,
 * seen from azimuth az (degrees from +z toward +x) and elevation el (camera above, looking down) */
export function frameKey(f: number, S: V3, sx: number, sy: number, h: number, frac: number, az: number, el: number, fov = 40, ease?: Ease, curve?: boolean): CamKey {
  const visH = h / frac, d = visH / (2 * Math.tan((fov * D2R) / 2)), visW = visH * ASPECT;
  const a = az * D2R, e = el * D2R;
  const fwd = new THREE.Vector3(-Math.sin(a) * Math.cos(e), -Math.sin(e), -Math.cos(a) * Math.cos(e));
  const right = new THREE.Vector3(Math.cos(a), 0, -Math.sin(a));
  const up = new THREE.Vector3().crossVectors(right, fwd);
  const look = new THREE.Vector3(...S).addScaledVector(right, -(sx - 0.5) * visW).addScaledVector(up, (sy - 0.5) * visH);
  const pos = look.clone().addScaledVector(fwd, -d);
  return { t: F(f), pos: pos.toArray() as V3, look: look.toArray() as V3, fov, ease: ease ?? "lin", curve };
}
const K = (f: number, pos: V3, look: V3, fov = 40, ease: Ease = "lin", curve = false): CamKey => ({ t: F(f), pos, look, fov, ease, curve });
/** a step track from [frame, value] pairs */
const steps = <T,>(keys: [number, T][]) => keys.map(([f, v]) => ({ t: F(f), v }));

const HEAD_Y = 1.375, HEAD_H = 0.59;                       // Actor: head centre above the feet, head height (scale 1)
const head = (p: V3, s = 1): V3 => [p[0], p[1] + HEAD_Y * s, p[2]];

const HALL: Preset = { ...PRESETS.golden, lit: [1.2, 1.08, 0.96], shade: [0.5, 0.5, 0.62], sat: 0.7, cardShade: [0.72, 0.68, 0.88], fog: "#5c5070", fogNear: 18, fogFar: 70, bg: "#3c3354", glow: 0.8 };
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
/** a ball falling from a dragon mouth into its frog (gravity, landing at f1); hidden after landing */
const fall = (i: number, f0: number, f1: number) => (t: number): V3 | null => {
  const fr = t * 30; if (fr >= f1) return null;
  const a = mouthOf(i), b = frogMouthOf(i);
  if (fr < f0) return a;
  const u = (fr - f0) / (f1 - f0);
  return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u * u, a[2] + (b[2] - a[2]) * u];
};

const DBG = (p: V3): Rig => (ctx) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.06), new THREE.MeshBasicMaterial({ color: "#ff0000", depthTest: false })); m.renderOrder = 99; m.position.set(...p); ctx.root.add(m); return () => {}; };
export function buildStudy(_T: Timing): StudyStory {
  const groups: GroupSpec[] = [];
  const INV: V3 = [-1.45, 0, 1.25];
  const INV2: V3 = [-0.55, 0, 2.55];
  const emperorSpec = (face: { t: number; v: string }[], pose: { t: number; v: string }[] = steps([[0, "stand"]])): PersonSpec =>
    ({ id: "emperor", scale: 1.05, at: () => EMPEROR, props: () => ({ costume: "persianLord", seed: 3, face, pose, blinks: [] }) });
  const guardSpecs = (face: { t: number; v: string }[], pose: { t: number; v: string }[] = steps([[0, "stand"]])): PersonSpec[] =>
    GUARDS.map((g, k) => ({ id: `guard${k}`, at: () => g, faceTo: () => EMPEROR, props: () => ({ costume: "hoplite", seed: 7 + k, face, pose, blinks: [] }) }));
  const JC: V3 = [JAR[0], 1.5, JAR[2]];

  // ===== shot 1, F0-F91 (one camera move): the inventor at the jar (smug), push into the dragon's mouth as the arm
  // leaves the ball, glint on "mouth", crane up over the jar lid to the emperor on his dais
  {
    const invFace = steps([[0, "smug"], [14, "stunned"]]);
    groups.push({
      id: "hook", place: "hall", t0: 0, t1: F(92), xfade: 0, set: hallSet, light: HALL, lens: { cInf: 18 },
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
        { id: "inventor", at: () => INV, faceTo: () => headOf(0), props: () => ({ costume: "master", seed: 1, face: invFace, pose: steps([[0, "holdHigh"]]), blinks: [] }) },
        emperorSpec(steps([[0, "frown"]])), ...guardSpecs(steps([[0, "frown"]])),
      ],
      rigs: [flamesRig(), ballRig((i) => mouthOf(i)), armRig([-1.15, 1.15, 1.35], mouthOf(0), 21, 36, 43),
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
      id: "warning", place: "hall", t0: F(92), t1: F(225), xfade: 0, join: { kind: "cut" }, set: hallSet, light: HALL, lens: { cInf: 16 },
      cam: [
        frameKey(92, head(INV), 0.36, 0.47, HEAD_H, 0.19, 4, 3),
        frameKey(142, head(INV), 0.37, 0.47, HEAD_H, 0.2, 4, 3, 40, "lin"),
        frameKey(150, head(INV), 0.55, 0.56, HEAD_H, 0.222, 0, 3, 40, "snap"),
        frameKey(158, head(INV), 0.58, 0.58, HEAD_H, 0.23, -2, 3, 40, "lin"),
        K(162, [-2.2, 2.0, 2.6], [1.5, 1.7, -5], 40, "in", true),
        K(166, [-1.9, 2.1, -3.0], [0, 1.95, THRONE_Z], 40, "lin", true),
        frameKey(170, empH, 0.48, 0.38, HEAD_H * 1.05, 0.21, 0, 2, 40, "out", true),
        frameKey(185, empH, 0.48, 0.38, HEAD_H * 1.05, 0.22, 0, 2, 40, "lin"),
        frameKey(200, empH, 0.5, 0.45, HEAD_H * 1.05, 0.07, 0, 7, 55, "io"),
        frameKey(225, empH, 0.5, 0.45, HEAD_H * 1.05, 0.075, 0, 7, 55, "lin"),
      ],
      people: [
        { id: "inventor", at: () => INV, faceTo: (t) => (t < F(143) ? headOf(0) : [-4, 2, 0]), props: () => ({ costume: "master", seed: 1, face: invFace, pose: invPose, blinks: [F(117)], marks: [{ t0: F(136), kind: "sweat" }] }) },
        emperorSpec(steps([[0, "frown"], [180, "grimace"], [183, "laugh"], [193, "cackle"]]), steps([[0, "stand"], [193, "laugh"]])),
        ...guardSpecs(steps([[0, "frown"], [186, "laugh"], [196, "cackle"]]), steps([[0, "stand"], [190, "laugh"]])),
      ],
      rigs: [flamesRig(), ballRig((i, t) => (i === 0 ? fall(0, 121, 131)(t) : mouthOf(i)))],
      alive: [[F(92), F(225)]],
    });
  }
  // ===== shot 3, F225-F404 (4 f dissolve in): the jar from high on the right, orbiting to the front and coming down
  // ("eight dragons coiled around a giant bronze jar"), a push to the front dragon, a tilt down to the frog's mouth
  {
    groups.push({
      id: "jar", place: "hall", t0: F(225), t1: F(405), xfade: 0, join: { kind: "dissolve", frames: 4 }, set: hallSet, light: HALL, lens: { cInf: 8 },
      cam: [
        frameKey(223, JC, 0.34, 0.42, 3.1, 0.45, 30, 22, 44),
        frameKey(300, JC, 0.36, 0.45, 3.1, 0.5, 16, 16, 44, "lin", true),
        frameKey(345, JC, 0.45, 0.52, 3.1, 0.66, 8, 10, 40, "lin", true),
        frameKey(362, [JC[0] + 0.15, 1.3, JC[2] + 1.05], 0.5, 0.5, 3.0, 1.05, 8, 2, 40, "io"),
        frameKey(382, frogMouthOf(1), 0.5, 0.75, 0.9, 0.4, 8, 4, 40, "io"),
        frameKey(406, frogMouthOf(1), 0.5, 0.75, 0.9, 0.42, 8, 4, 40, "lin"),
      ],
      people: [emperorSpec(steps([[0, "frown"]])), ...guardSpecs(steps([[0, "frown"]]))],
      rigs: [flamesRig(), ballRig((i) => mouthOf(i))],
      alive: [[F(225), F(405)]],
    });
  }
  // ===== shot 4, F405-F535 (6 f dissolve in): the emperor on his balcony; on "biggest" the camera cranes up over his
  // head to the army filling the parade ground, holds, and comes back down to his frown for "from a jar."
  {
    const H = head(BAL_EMP, 1.05);
    groups.push({
      id: "balcony", place: "balcony", t0: F(405), t1: F(536), xfade: 0, join: { kind: "dissolve", frames: 6 }, set: balconySet, light: DAY, lens: { cInf: 4 },
      cam: [
        frameKey(402, H, 0.6, 0.42, HEAD_H * 1.05, 0.14, -8, 2),
        frameKey(427, H, 0.58, 0.42, HEAD_H * 1.05, 0.145, -8, 2, 40, "lin"),
        K(432, [0.25, 5.2, 7.6], [0, -4, -40], 40, "in", true),
        K(441, [0.2, 7.5, 11], [0, -11, -50], 40, "out", true),
        K(497, [0.2, 7.3, 10.4], [0, -11, -50], 40, "lin"),
        K(504, [0.3, 4.6, 6.8], [0, -1, -40], 40, "in", true),
        frameKey(512, H, 0.55, 0.42, HEAD_H * 1.05, 0.13, 5, 2, 40, "out", true),
        frameKey(540, H, 0.55, 0.42, HEAD_H * 1.05, 0.135, 5, 2, 40, "lin"),
      ],
      people: [{ id: "emperor", scale: 1.05, at: () => BAL_EMP, props: () => ({ costume: "persianLord", seed: 3, face: steps([[0, "frown"], [503, "angry"], [512, "frown"]]), pose: steps([[0, "stand"]]), blinks: [F(470)] }) }],
      alive: [[F(405), F(536)]],
    });
  }
  // ===== shot 5, F536-F599 (5 f dissolve in): weeks later, the inventor dozing at the jar; a ball drops into a frog
  // with an impact burst on "fell,", he jolts awake; the camera starts a fast push to the right
  {
    groups.push({
      id: "later", place: "hall", t0: F(536), t1: F(600), xfade: 0, join: { kind: "dissolve", frames: 5 }, set: hallSet, light: HALL, lens: { cInf: 14 },
      cam: [
        frameKey(534, head(INV2), 0.27, 0.6, HEAD_H, 0.09, -12, 9),
        frameKey(594, head(INV2), 0.3, 0.58, HEAD_H, 0.1, -12, 9, 40, "lin"),
        frameKey(603, head(INV2), 0.05, 0.6, HEAD_H, 0.19, 14, 6, 40, "out"),
      ],
      people: [{ id: "inventor", at: () => INV2, faceTo: () => headOf(1), props: () => ({ costume: "master", seed: 1, face: steps([[0, "sleepy"], [570, "stunned"], [575, "grimace"], [585, "stunned"], [594, "sly"]]), pose: steps([[0, "stand"], [570, "shrug"], [580, "stand"]]), blinks: [] }) }],
      rigs: [flamesRig(), ballRig((i, t) => (i === 1 ? fall(1, 555, 569)(t) : mouthOf(i))), burst([{ at: frogMouthOf(1), t: F(569), size: 0.9, n: 10 }])],
      alive: [[F(536), F(600)]],
    });
  }
  return { groups };
}
