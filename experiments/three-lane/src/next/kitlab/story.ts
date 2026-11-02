// KitLab story (our own code, lab content): 14 shot groups in ~37 s that put every new piece on screen, word-anchored
// on the synthetic narration (script.ts). Each group notes which rule-book piece it proves.
import * as THREE from "three";
import type { V3, Rig } from "../../kit/Stage";
import type { Timing } from "../../kit/timing";
import { fit, personBox, setRoom, sm, type Box } from "../../kit/framing";
import { lambert, box as mkBox } from "../../kit/sets";
import { NOINK } from "../../ink";
import { Rising } from "../../kit/fx";
import { actorRig, actorsToPeople } from "../../kit/actorCard";
import { castKey } from "../../kit/castframe";
import type { CamKey } from "../../kit/campath";
import { faceTrack, poseTrack, wordT, markAt, fillAt, checkFaceTrack, type Word, type FaceKey } from "../../kit/acting";
import { crossSectionSet, macroSet, mapSet, routeRig, blueprintSet, drawOnRig, xraySet, xrayPanel } from "../../kit/cutaways";
import { glints, burst, debris, counter, scan } from "../../kit/fx2";
import { lightArc } from "../../kit/lightarc";
import { boxRect, matchKey, quadPortal, circlePortal, quadAt } from "../../kit/match";
import type { GroupSpec as NextGroup } from "../../kit/Stage";
import type { Story as NextStory } from "../../kit/Episode3D";
import { SENTENCES } from "./script";
import { roomSet, gearRoomSet, seaSet, deckSet, xrayCanvases, gear, brassKey, weight, photoQuad, windowQuad, clockHands, ROOM } from "./sets";

export type LabStory = NextStory & { cast: Record<string, (t: number) => V3[]>; pov: { t0: number; t1: number }; faceReport: ReturnType<typeof checkFaceTrack>; adaHead: (t: number) => Box | null };

const KS = 0.0025;                                                // Actor svg unit -> metres (PERSON_K, scale 1)
const headBox = (p: V3): Box => [p[0] - 0.3, p[1] + 1.08, p[2] - 0.1, p[0] + 0.3, p[1] + 1.68, p[2] + 0.1];
const upperBox = (p: V3): Box => personBox(p, false, true);
const ROOMBOX: Box = [-3.9, 0.1, -5.9, 3.9, 4.1, 1.9];
const CLOCKBOX: Box = [ROOM.clock[0] - 0.9, ROOM.clock[1] - 0.9, -5.9, ROOM.clock[0] + 0.9, ROOM.clock[1] + 0.9, -5.6];
const roomFit = (...a: Parameters<typeof fit>) => { setRoom(ROOMBOX); const k = fit(...a); setRoom(null); return k; };
/** a framing solved with the room constraint on (castKey uses framing.fit) */
const room = (f: () => CamKey): CamKey => { setRoom(ROOMBOX); const k = f(); setRoom(null); return k; };
/** a mesh rig: build once, update per frame */
const meshRig = (build: (root: THREE.Group) => (t: number) => void): Rig => (ctx) => build(ctx.root);

export function buildLab(T: Timing): LabStory {
  const words = T.words as Word[];
  const w = (word: string, n = 1, after = -1) => wordT(words, word, n, after);
  // sentence starts (S[i]) from the script's word counts
  const S: number[] = []; let wi = 0;
  for (const s of SENTENCES) { S.push(words[wi].start); wi += s.split(/\s+/).length; }
  const END = words[words.length - 1].end + 0.4;
  const groups: NextGroup[] = [];
  const ada = { costume: "keeper", seed: 4 };
  const adaFaces: FaceKey[] = [];
  const heads: { t0: number; t1: number; at: V3 }[] = [];
  const cast: Record<string, (t: number) => V3[]> = {};

  // ---------------------------------------------------------------- 1 lamp room, golden: the hook (faces on words, prop swing)
  {
    const t0 = 0, t1 = S[1], A: V3 = [0.5, 0, -5.0];
    const faces = faceTrack(words, "deadpan", [{ word: "wind", face: "focus" }, { word: "hand.", face: "bliss" }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A });
    groups.push({
      id: "room-golden", place: "room", t0, t1, xfade: 0, set: () => roomSet(), light: "golden",
      cam: [room(() => castKey(t0, [A], "wide", -25, 6, 38, 1, [CLOCKBOX], ROOMBOX)), room(() => castKey(w("lighthouse"), [A], "close", 22, 4, 34, 1, [], ROOMBOX))],
      people: [],
      rigs: [
        actorRig({ id: "ada", at: () => A, faceTo: () => ROOM.clock, props: () => ({ ...ada, face: faces, pose: poseTrack(words, "hold", [["climbed", "holdHigh"], ["wind", "wind"]], t0), item: "key" }) }),
        (ctx) => (t) => clockHands(ctx.set, 9.2 + t * 0.02),
      ],
    });
  }
  // ---------------------------------------------------------------- 2 macro insert: the brass key, a glint on "key"
  const keyBow: Box = [-0.065, 0.0, -0.065, 0.065, 0.04, 0.065];
  {
    const t0 = S[1], t1 = S[2];
    groups.push({
      id: "macro-key", place: "macro", insert: true, lens: { cInf: 22 }, t0, t1, xfade: 0.4, set: () => macroSet({ surface: "cloth" }), light: "golden",
      cam: [fit(t0, [[-0.07, 0, -0.07, 0.24, 0.05, 0.1]], 24, 32, 30, { b: 0.36, t: 0.2, x: 0.1 }), fit(w("older"), [[-0.07, 0, -0.07, 0.12, 0.05, 0.07]], -14, 40, 28, { b: 0.42, t: 0.24, x: 0.14 })],
      people: [],
      rigs: [meshRig((root) => { const k = brassKey(1); k.rotation.y = -0.35; k.position.y = 0.012; root.add(k); return () => {}; }),
        glints([{ at: [0.0, 0.05, 0.02], t: w("key"), size: 0.07, life: 9 }])],
    });
  }
  // ---------------------------------------------------------------- 3 cross-section insert (match dissolve key -> stone)
  const stoneY = (t: number) => -1.55 - 0.14 * sm((t - w("dropped")) / 0.45);
  const tower: Rig = (ctx) => {
    const root = ctx.root, wall = lambert({ color: "#c9b79c" });
    mkBox(root, wall, 3.0, 4.2, 0.2, 0, 2.1, -1.7); mkBox(root, wall, 0.2, 4.2, 1.7, -1.5, 2.1, -0.85); mkBox(root, wall, 0.2, 4.2, 1.7, 1.5, 2.1, -0.85);
    mkBox(root, lambert({ color: "#8a5a3a" }), 3.4, 0.3, 2.0, 0, 4.35, -0.85);
    const g1 = gear(0.55, 14, 0.12); g1.position.set(-0.45, 1.6, -0.9); root.add(g1);
    const g2 = gear(0.34, 9, 0.12); g2.position.set(0.48, 2.35, -0.9); root.add(g2);
    // the weight hangs from a pulley at y 3.0 inside the tower; the rope shortens as the stone drops
    const pul = gear(0.14, 8, 0.08); pul.position.set(0, 3.0, -0.5); root.add(pul);
    const { g } = weight(1); g.position.set(0, 3.0, -0.5); root.add(g);
    const [rope, stone, ring] = g.children;
    return (t) => {
      g1.rotation.z = -t * 0.35; g2.rotation.z = t * 0.35 * (14 / 9) + 0.2; pul.rotation.z = -t * 0.5;
      const L = 3.0 - (stoneY(t) + 0.25);
      rope.scale.y = L; rope.position.y = -L / 2; stone.position.y = -L - 0.25; ring.position.y = -L + 0.02;
    };
  };
  const stoneBox = (t: number): Box => [-0.32, stoneY(t) - 0.25, -0.82, 0.32, stoneY(t) + 0.25, -0.18];
  {
    const t0 = S[2], t1 = S[3];
    const gm = groups[groups.length - 1];
    const tgt = boxRect(gm, t0, keyBow);
    groups.push({
      id: "xsection", place: "cross-section", insert: true, t0, t1, xfade: 0, set: () => crossSectionSet({ cavity: { x: 0, y: -0.15, w: 1.1, h: 2.4, d: 1.0 }, frame: true, width: 7 }), light: "day",
      join: { kind: "match", frames: 7, anchor: (t) => { const r = boxRect(groups[2], t, stoneBox(t)); return [r.cx, r.cy]; } },
      cam: [matchKey(t0, stoneBox(t0), { cx: tgt.cx, cy: tgt.cy, h: tgt.h }, 0, 4, 34),
        { ...fit(w("hour,"), [[-2.6, -2.8, -1.8, 2.6, 4.5, 0.2]], 8, 5, 40, { b: 0.06, t: 0.06 }), drift: 0.6 },
        fit(w("turned"), [[-1.1, 0.95, -1.0, 0.85, 2.75, -0.8]], -12, 6, 36, { b: 0.3, t: 0.16 })],
      people: [],
      rigs: [tower, counter({ at: [2.45, 3.0, 0.15], w: 1.0, digits: 4, from: 0, to: 0, t0: 0, t1: 1, steps: [[t0, 41], [w("inch"), 42]], label: "INCHES FALLEN" }),
        glints([{ at: (t) => [0.25, stoneY(t) + 0.2, -0.2], t: w("stone"), size: 0.35 }])],
    });
  }
  // ---------------------------------------------------------------- 4 blueprint insert (match dissolve gear -> drawn gear)
  const BW = 2.4, BD = 1.7;
  const sheetPt = (u: number, v: number): V3 => {         // sheet uv (v from the top edge) -> world (board tilted -0.32 rad)
    const x = (u - 0.5) * BW, z = (v - 0.5) * BD, c = Math.cos(-0.32), s = Math.sin(-0.32);
    return [x, 0.9 + (0.0 * c - z * s), 0.0 * s + z * c];
  };
  const circ = (cu: number, cv: number, r: number, teeth = 0): [number, number][] => Array.from({ length: (teeth || 24) * 4 + 1 }, (_, i) => {
    const n = (teeth || 24) * 4, a = (i / n) * Math.PI * 2, k = teeth && Math.floor(i / 2) % 2 ? 1.14 : 1;
    return [cu + Math.cos(a) * r * k, cv + Math.sin(a) * r * k * (BW / BD)] as [number, number];
  });
  {
    const t0 = S[3], t1 = S[4];
    const gx = groups[groups.length - 1];
    const gearOut: Box = [-0.45 - 0.62, 1.6 - 0.62, -0.96, -0.45 + 0.62, 1.6 + 0.62, -0.84];
    const tgt = boxRect(gx, t0, gearOut);
    const gc = sheetPt(0.3, 0.42), r = 0.13 * BW;
    const gBox: Box = [gc[0] - r, gc[1] - r * 0.4, gc[2] - r * 0.95, gc[0] + r, gc[1] + r * 0.4, gc[2] + r * 0.95];
    const lines = [circ(0.3, 0.42, 0.13, 14), circ(0.3, 0.42, 0.03), circ(0.52, 0.28, 0.08, 9), circ(0.52, 0.28, 0.02),
      [[0.6, 0.3], [0.6, 0.78]] as [number, number][], [[0.56, 0.78], [0.64, 0.78], [0.66, 0.9], [0.54, 0.9], [0.56, 0.78]] as [number, number][],
      [[0.1, 0.1], [0.75, 0.1], [0.75, 0.95], [0.1, 0.95], [0.1, 0.1]] as [number, number][]];
    groups.push({
      id: "blueprint", place: "blueprint", insert: true, t0, t1, xfade: 0, light: "museum",
      set: () => blueprintSet({ lines, title: "CLOCK No. 1", notes: [{ text: "WEIGHT 40 LB", u: 0.67, v: 0.86 }, { text: "TRAIN 14 : 9", u: 0.58, v: 0.2 }], w: BW, d: BD }),
      join: { kind: "match", frames: 7, anchor: (t) => { const q = boxRect(groups[3], t, gBox); return [q.cx, q.cy]; } },
      cam: [matchKey(t0, gBox, { cx: tgt.cx, cy: tgt.cy, h: tgt.h }, 0, 62, 34), { ...fit(w("mechanism"), [[-1.25, 0.6, -0.9, 1.25, 1.2, 0.9]], 6, 58, 38, { b: 0.08, t: 0.08 }), drift: 0.6 }],
      people: [],
      rigs: [drawOnRig(t0 - 2.0, w("sheet") + 0.2)],
    });
  }
  // ---------------------------------------------------------------- 5 map insert: route draws on, a rolling counter
  {
    const t0 = S[4], t1 = S[5];
    groups.push({
      id: "map", place: "map", insert: true, t0, t1, xfade: 0.4, light: "golden",
      set: () => mapSet({ places: [{ name: "LIGHTHOUSE", u: 0.2, v: 0.72 }, { name: "PORT", u: 0.8, v: 0.3 }], route: [[0.2, 0.72], [0.33, 0.62], [0.47, 0.6], [0.6, 0.44], [0.8, 0.3]], title: "THE NORTH CHANNEL" }),
      cam: [fit(t0, [[-1.7, 0.8, -1.2, 1.7, 0.85, 1.2]], 0, 64, 36, { b: 0.1, t: 0.1, x: 0.04 }), fit(w("bell"), [[-1.0, 0.8, -1.0, 1.7, 1.3, 1.1]], 18, 46, 36, { b: 0.1, t: 0.1 })],
      people: [],
      rigs: [routeRig(t0 + 0.1, w("out.") - 0.05, [t0, w("out.")]),
        counter({ at: [1.45, 1.05, 1.05], rotY: -0.2, w: 0.6, digits: 2, from: 0, to: 40, t0: w("forty"), t1: w("out."), label: "MILES" }),
        glints([{ at: [(0.8 - 0.5) * 3.4, 1.0, (0.3 - 0.5) * 2.4], t: w("out."), size: 0.3 }])],
    });
  }
  // ---------------------------------------------------------------- 6 lamp room at night: alarm on "stopped", terrified, push into the eye
  const A6: V3 = [0.15, 0, -4.4];
  let EYE6: V3 = [0, 0, 0], YAW6 = 0;
  {
    const t0 = S[5], t1 = S[7];
    const faces = faceTrack(words, "worried", [{ word: "stopped.", face: "stunned" }, { word: "terrified.", face: "terrified", react: [{ face: "blank", frames: 2 }] }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A6 });
    // the push into the eye: Ada's card is held at a fixed yaw (not a billboard) so her eye is a fixed world point,
    // and the camera aims at that point from k1 and flies straight through it (no hold orbit on k1)
    const k1f = roomFit(w("Ada", 2) - 0.05, [headBox(A6)], 4, 2, 30, { b: 0.78, t: 0.1, x: 0.18 });
    const yaw6 = Math.atan2(k1f.pos[0] - A6[0], k1f.pos[2] - A6[2]);
    EYE6 = [A6[0] + Math.cos(yaw6) * (387 - 300) * KS, A6[1] + (700 - 141.6) * KS, A6[2] - Math.sin(yaw6) * (387 - 300) * KS];
    const eye = EYE6;
    const d1 = new THREE.Vector3(...k1f.pos).distanceTo(new THREE.Vector3(...eye));
    const n = new THREE.Vector3(Math.sin(yaw6), 0.08, Math.cos(yaw6)).normalize();
    const k1 = { t: k1f.t, pos: [eye[0] + n.x * d1, eye[1] + n.y * d1, eye[2] + n.z * d1] as V3, look: [eye[0], eye[1] - 0.3, eye[2]] as V3, fov: 30, drift: 0 };   // aimed under the eye: the face sits above the caption band
    const k2 = { t: t1, pos: [eye[0] - n.x * 0.15, eye[1] - n.y * 0.15, eye[2] - n.z * 0.15] as V3, look: [eye[0] - n.x * 2, eye[1] - n.y * 2, eye[2] - n.z * 2] as V3, fov: 30, glide: 0.75 };
    YAW6 = yaw6;
    groups.push({
      id: "room-night", place: "room", t0, t1, xfade: 0.4, set: () => roomSet({ night: true }),
      light: lightArc([[t0, "night"]], [{ kind: "alarm", t: w("stopped."), dur: 1.0, every: 6 }]),
      cam: [room(() => castKey(t0, [A6], "medium", 12, 8, 40, 1, [], ROOMBOX)), k1, k2],
      people: [],
      rigs: [actorRig({ id: "ada", at: () => A6, billboard: false, yaw: YAW6, props: () => ({ ...ada, face: faces, blinks: [t0 + 0.6], pose: poseTrack(words, "stand", [["stopped.", "shrug"], ["terrified.", "cheeks"]], t0),
        marks: [markAt(words, "stopped.", "sweat")], fill: [fillAt(words, "terrified.", "#8a63d2")] }) }),
        (ctx) => (t) => clockHands(ctx.set, 2.75 + Math.min(t, w("stopped.")) * 0.05)],
    });
  }
  // ---------------------------------------------------------------- 7 x-ray insert (pushed in through the eye): scan-line reveal
  {
    const t0 = S[7], t1 = S[8];
    const room = groups[groups.length - 1];
    groups.push({
      id: "xray", place: "x-ray", insert: true, t0, t1, xfade: 0, set: () => xraySet(xrayCanvases()), light: "explain",
      join: { kind: "push", frames: 16, portal: circlePortal(room, () => [EYE6[0], EYE6[1], EYE6[2] + 0.004], 0.05) },
      cam: [{ t: t0, pos: [0, 1.6, 2.0], look: [0, 1.55, 0], fov: 40 }, { t: w("snapped"), pos: [0.15, 1.36, 1.05], look: [0.15, 1.33, 0], fov: 34 }],
      people: [],
      rigs: [(ctx) => scan(xrayPanel(ctx.set), w("casing,"), 9, 1)(ctx), burst([{ at: [0.15, 1.325, 0.05], t: w("snapped"), size: 0.45, n: 10 }])],
    });
  }
  // ---------------------------------------------------------------- 8 inside the clock: the strike (burst, debris, flash, steam, swing)
  {
    const t0 = S[8], t1 = S[9], A: V3 = [-0.95, 0.2, -3.05];
    const slot: V3 = [1.4 + Math.cos(Math.PI) * 1.51, 1.5, -3.5];
    const hit = w("hammered");
    const faces = faceTrack(words, "focus", [{ word: "hammered", face: "furious", react: [{ face: "squeeze", frames: 2 }] }, { word: "place.", face: "bliss" }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A });
    groups.push({
      id: "gears", place: "inside clock", t0, t1, xfade: 0.4, set: gearRoomSet,
      light: lightArc([[t0, "night"]], [{ kind: "flash", t: hit, frames: 2 }]),
      cam: [castKey(t0, [A], "wide", -18, 8, 40, 1, [[slot[0] - 0.3, 1.0, -3.7, 2.9, 3.0, -3.4]]), castKey(hit - 0.35, [A], "medium", 16, 4, 34, 1, [[slot[0] - 0.2, 1.3, -3.6, slot[0] + 0.2, 1.7, -3.4]])],
      people: [],
      rigs: [
        (ctx) => {
          const { big, mid, small, tooth } = ctx.set.extra;
          return (t) => {
            const go = Math.max(0, t - w("back"));
            const a = go > 0 ? go * go / (go + 0.4) * 0.9 : 0;               // eased start
            big.rotation.z = Math.PI / 2 - a; mid.rotation.z = a * (28 / 16); small.rotation.z = -a * (28 / 10) + 0.1;
            if (t < hit) { tooth.position.set(-0.45, 0.34, -2.75); tooth.rotation.set(0.2, 0.5, 1.2); }
            else { const p = new THREE.Vector3(slot[0], slot[1], -3.5).sub(new THREE.Vector3(1.4, 1.5, -3.5)).applyAxisAngle(new THREE.Vector3(0, 0, 1), -a).add(new THREE.Vector3(1.4, 1.5, -3.5)); tooth.position.copy(p); tooth.rotation.set(0, 0, -a); }
          };
        },
        actorRig({ id: "ada", at: () => A, faceTo: () => slot, props: () => ({ ...ada, face: faces, item: "hammer", pose: [{ t: t0, v: "hold" }, { t: w("and", 1, t0) - 0.07, v: "strikeUp" }, { t: hit - 2 / 30, v: "strike" }, { t: w("place.") - 0.07, v: "hips" }],
          marks: [{ t0: hit, t1: hit + 1.1, kind: "steam" }] }) }),
        burst([{ at: slot, t: hit, size: 1.1, n: 14 }]),
        debris([{ at: slot, t: hit, n: 28, kind: "splinter", size: 0.14, speed: 2.6, floorY: 0.2, life: 1.3 }]),
        meshRig((root) => { const puff = new Rising(6, "puff", 0.22, 3); puff.group.position.set(slot[0], 1.2, -3.3); root.add(puff.group); return (t) => puff.update(t, t > hit && t < hit + 0.8 ? 1 : 0, 0.6, 0.8, 0.5); }),
      ],
    });
  }
  // ---------------------------------------------------------------- 9 lamp room at night: push through the window into the sea
  {
    const t0 = S[9], t1 = w("ship"), A: V3 = [-3.3, 0, -0.95];
    const faces = faceTrack(words, "focus", [{ word: "saw", face: "worried" }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A });
    groups.push({
      id: "room-window", place: "room", establishing: true, t0, t1, xfade: 0.4, set: () => roomSet({ night: true }), light: "night",
      cam: [{ t: t0, pos: [0.4, 1.55, 1.3], look: [-3.0, 1.15, -2.4], fov: 40 }, { t: t1, pos: [-4.7, 2.05, -2.6], look: [-9, 2.05, -2.6], fov: 40, glide: 1.0 }],
      people: [],
      rigs: [actorRig({ id: "ada", at: () => A, faceTo: () => ROOM.window, props: () => ({ ...ada, face: faces, item: "lantern", pose: poseTrack(words, "hold", [["window,", "holdHigh"]], t0) }) })],
    });
  }
  // ---------------------------------------------------------------- 10 POV through a spyglass: the ship turns for the rocks
  const povT = { t0: w("ship"), t1: S[10] };
  {
    const t0 = povT.t0, t1 = povT.t1, room = groups[groups.length - 1];
    groups.push({
      id: "sea-pov", place: "sea", insert: true, t0, t1, xfade: 0.4, set: seaSet, light: "night",
      join: { kind: "push", frames: Math.round((t0 - room.t0) * 30) - 6, portal: quadPortal(room, windowQuad()) },
      cam: [{ t: t0, pos: [0, 16, 24], look: [9, 2, -62], fov: 22, drift: 0.5 }, { t: w("rocks."), pos: [0, 16, 24], look: [3, 2, -36], fov: 22, drift: 0.5 }],
      people: [],
      rigs: [(ctx) => { const ship = ctx.set.extra.ship, water = ctx.set.extra.water; const map = (water as THREE.Mesh<THREE.BufferGeometry, THREE.MeshLambertMaterial>).material.map!;
        return (t) => { const u = sm((t - t0) / (t1 - t0 + 0.6)); ship.position.set(10 - 7 * u, 0, -70 + 22 * u); ship.rotation.y = 0.2 + 0.9 * u; map.offset.set(t * 0.004, t * 0.002); }; }],
    });
  }
  // ---------------------------------------------------------------- 11 the bell: night relights to dawn inside the shot; tears, then bliss
  {
    const t0 = S[10], t1 = S[11], A: V3 = [2.45, 0, -4.35];
    const faces = faceTrack(words, "worried", [{ word: "rang", face: "sob" }, { word: "dawn.", face: "bliss" }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A });
    groups.push({
      id: "bell", place: "room", t0, t1, xfade: 0.4, set: () => roomSet({ night: true }),
      light: lightArc([[t0, "night"], [w("until"), "dawn", 0.8]], [{ kind: "ramp", t: w("dawn."), dur: 0.5, to: "golden" }]),
      cam: [room(() => castKey(t0, [A], "medium", -14, 6, 38, 1, [], ROOMBOX)), room(() => castKey(w("until"), [A], "close", 22, 4, 34, 1, [], ROOMBOX))],
      people: [],
      rigs: [actorRig({ id: "ada", at: () => A, faceTo: () => ROOM.rope, props: () => ({ ...ada, face: faces,
        pose: poseTrack(words, "reach", [["rang", "armsUp"], ["bell", "reach"], ["hand", "armsUp"], ["until", "reach"], ["dawn.", "hips"]], t0, 1),
        marks: [{ t0: w("rang"), t1: w("dawn."), kind: "tears" }, markAt(words, "dawn.", "blush")] }) }),
        meshRig((root) => { const tassel = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.2, 8), lambert({ color: "#c8402e" })); root.add(tassel);
          const pulls = [w("rang"), w("bell"), w("hand"), w("until")];
          return (t) => { const last = pulls.filter((p) => t >= p).pop(); const f = last === undefined ? 99 : (t - last) * 30; tassel.position.set(ROOM.rope[0], 1.0 - (f < 4 ? 0.18 * (f / 4) : f < 14 ? 0.18 * (1 - (f - 4) / 10) : 0), ROOM.rope[2]); }; })],
    });
  }
  // ---------------------------------------------------------------- 12 day: the photograph on the table (glint), the crew grows out of it
  const PHOTO_C: V3 = [-2.0, 1.12, -5.0];
  const tablePhoto = (): V3[] => {      // the picture area (9:16) of a frame standing on the table, leaning back 12 degrees
    const w2 = 0.09, h2 = 0.16, lean = 0.21;
    const up = new THREE.Vector3(0, Math.cos(lean), -Math.sin(lean)), rt = new THREE.Vector3(1, 0, 0), c = new THREE.Vector3(...PHOTO_C).add(new THREE.Vector3(0, 0, 0.012));
    return [c.clone().addScaledVector(rt, -w2).addScaledVector(up, h2), c.clone().addScaledVector(rt, w2).addScaledVector(up, h2), c.clone().addScaledVector(rt, w2).addScaledVector(up, -h2), c.clone().addScaledVector(rt, -w2).addScaledVector(up, -h2)].map((v) => [v.x, v.y, v.z] as V3);
  };
  {
    const t0 = S[11], t1 = w("of", 1, S[11]), A: V3 = [-1.35, 0, -4.4];
    const faces = faceTrack(words, "smile", [{ word: "photograph", face: "bliss" }], t0);
    adaFaces.push(...faces); heads.push({ t0, t1, at: A });
    const photoBox: Box = [PHOTO_C[0] - 0.12, PHOTO_C[1] - 0.2, PHOTO_C[2] - 0.05, PHOTO_C[0] + 0.12, PHOTO_C[1] + 0.2, PHOTO_C[2] + 0.05];
    groups.push({
      id: "room-photo", place: "room", insert: true, t0, t1, xfade: 0.4, set: () => roomSet(), light: "day",
      cam: [room(() => castKey(t0, [A], "medium", 12, 10, 38, 1, [photoBox], ROOMBOX)), { ...roomFit(w("photograph") - 0.15, [photoBox], 0, 6, 30, { b: 0.42, t: 0.3, x: 0.3 }), glide: 0.8 }],
      people: [],
      rigs: [actorRig({ id: "ada", at: () => A, faceTo: () => PHOTO_C, props: () => ({ ...ada, face: faces, pose: poseTrack(words, "hips", [["photograph", "point"]], t0), marks: [markAt(words, "photograph", "blush")] }) }),
        meshRig((root) => {
          const g = new THREE.Group(); g.position.set(PHOTO_C[0], PHOTO_C[1], PHOTO_C[2]); g.rotation.x = -0.21; root.add(g);
          mkBox(g, lambert({ color: "#3b2a3e" }), 0.25, 0.4, 0.02, 0, 0, 0);
          const pc = document.createElement("canvas"); pc.width = 90; pc.height = 160; const q = pc.getContext("2d")!;
          q.fillStyle = "#d8c49a"; q.fillRect(0, 0, 90, 160); q.fillStyle = "#a88c60"; q.fillRect(10, 90, 70, 60);
          const tx = new THREE.CanvasTexture(pc); tx.colorSpace = THREE.SRGBColorSpace;
          const pic = new THREE.Mesh(new THREE.PlaneGeometry(0.18, 0.32), lambert({ map: tx })); pic.position.z = 0.012; g.add(pic);
          const strut = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.3, 0.02), lambert({ color: "#3b2a3e" })); strut.position.set(0, -0.06, -0.08); strut.rotation.x = 0.6; g.add(strut);
          return () => {};
        }),
        glints([{ at: [PHOTO_C[0] + 0.1, PHOTO_C[1] + 0.17, PHOTO_C[2] + 0.04], t: w("photograph"), size: 0.12 }])],
    });
  }
  // ---------------------------------------------------------------- 13 the crew on deck (grown out of the photo): staggered reactions, a hat pop
  {
    const t0 = w("of", 1, S[11]), t1 = S[12];
    const prev = groups[groups.length - 1];
    const crew: { id: string; at: V3; costume: string; face: string; lag: number; react: string; flip?: boolean; pose: string }[] = [
      { id: "captain", at: [0, 0, -1.6], costume: "captain", face: "grin", lag: 0, react: "cackle", pose: "hips" },
      { id: "s1", at: [-0.9, 0, -1.85], costume: "sailor", face: "smile", lag: 8, react: "bliss", pose: "armsUp" },
      { id: "s2", at: [0.9, 0, -1.85], costume: "sailor2", face: "smile", lag: 15, react: "laugh", flip: true, pose: "point" },
    ];
    groups.push({
      id: "deck", place: "deck", t0, t1, xfade: 0, set: deckSet, light: "day",
      join: { kind: "outOf", frames: 12, quad: quadAt(prev, tablePhoto()), pre: 0.35 },
      cam: [castKey(t0, crew.map((c) => c.at), "medium", 0, 4, 36), castKey(w("harbour."), crew.map((c) => c.at), "medium", 16, 6, 34)],
      people: [],
      rigs: (cast["deck"] = () => crew.map((c) => c.at), crew.map((c) => {
        const faces = faceTrack(words, c.face, [{ word: "safe", face: c.react, lead: -c.lag }], t0);
        return actorRig({ id: c.id, at: () => c.at, flip: c.flip, props: () => ({ costume: c.costume, seed: c.lag + 2, face: faces, pose: c.pose, ...(c.id === "s2" ? { hatPop: [wordT(words, "safe") + c.lag / 30] } : {}) }) });
      })),
    });
  }
  // ---------------------------------------------------------------- 14 the crew shrinks into the frame on the wall beside the clock
  {
    const t0 = S[12], t1 = END;
    const pq = photoQuad();
    const pBox: Box = [pq[0][0], pq[2][1], -5.9, pq[1][0], pq[0][1], -5.8];
    groups.push({
      id: "room-wall", place: "room", t0, t1, xfade: 0, set: () => roomSet(), light: lightArc([[t0, "day"], [w("clock."), "golden", 0.5]]),
      join: { kind: "into", frames: 14, quad: (t) => quadAt(groups[13], pq)(t) },
      cam: [roomFit(t0, [pBox], 0, 2, 34, { b: 0.42, t: 0.2, x: 0.22 }), roomFit(w("beside"), [pBox, CLOCKBOX], -10, 3, 40, { b: 0.38, t: 0.12, x: 0.08 })],
      people: [],
      rigs: [(ctx) => (t) => clockHands(ctx.set, 8.0 + t * 0.03)],
    });
  }
  // the lead's face track over the whole lab, for the acting check
  const lead = [...adaFaces].sort((a, b) => a.t - b.t);
  const adaHead = (t: number): Box | null => { const h = heads.find((x) => t >= x.t0 && t < x.t1); return h ? headBox(h.at) : null; };
  void NOINK;
  for (const h of heads) { const g = groups.find((q) => q.t0 <= h.t0 + 1e-6 && q.t1 >= h.t1 - 1e-6); if (g && !cast[g.id]) cast[g.id] = () => [h.at]; }
  actorsToPeople(groups);
  return { groups, cast, pov: povT, faceReport: checkFaceTrack(lead, 0, END), adaHead };
}
