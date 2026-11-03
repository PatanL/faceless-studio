// story-barca-shield (our own code): Barca, c. 515 BC. A bronze-smith walks the inside of the wall laying his shield on
// the ground; where it rings, the Persians are tunnelling under. Shot groups word-anchored on the Kokoro timings,
// following episodes/story-barca-shield/shot_plan.md: castKey presets for people, the macro shield and the
// cross-section as inserts, faces swapped on words, a light arc, whips between places, no HUD.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../kit/Stage";
import type { Timing } from "../kit/timing";
import { fit as fit0, personBox, sm, tagSprite, setRoom, type Box } from "../kit/framing";
import { castKey } from "../kit/castframe";
import { crowd } from "../kit/density";
import type { CamKey } from "../kit/campath";
import { faceTrack, poseTrack, wordT, markAt, type Word } from "../kit/acting";
import { mapSet, routeRig } from "../kit/cutaways";
import { glints, burst, debris, counter } from "../kit/fx2";
import { lightArc, mixKey } from "../kit/lightarc";
import { Rising } from "../kit/fx";
import { barcaSet, shieldMacroSet, sectionSet, shieldMesh, SEC, WALL, CAMP } from "./sets";

export type BarcaStory = { groups: GroupSpec[] };

const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
// inside the city the camera stays between the house fronts and the wall, or above the roofs (first stills: a view
// solved from behind the houses looked through a house wall)
const CITY: Box = [-40, 0.3, -10.2, 44, 60, -1.7];
let ROOM: Box | null = null;
const fit = (...a: Parameters<typeof fit0>) => { setRoom(ROOM); const k = fit0(...a); setRoom(null); return k; };
/** castKey with a gentler hold drift on close and medium framings (the hold's push-in and orbit cropped heads at the
 * top edge and walked figures out at the sides in the first gate run) */
const cK = (...a: Parameters<typeof castKey>) => { setRoom(ROOM); const k0 = castKey(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7] ?? [], a[8] ?? ROOM ?? undefined); setRoom(null); const k = k0; return a[2] === "wide" ? k : { ...k, drift: a[2] === "close" ? 0.9 : 1.1 }; };
/** a world shield lying on the ground at p while visible(t) */
const groundShield = (p: V3, visible: (t: number) => boolean = () => true, R = 0.42): Rig => (ctx) => {
  const s = shieldMesh(R); s.position.set(...p); ctx.root.add(s);
  return (t) => { s.visible = visible(t); };
};
/** dust rings left in the dirt where the shield has been (they appear as he lifts it) */
const dustRings = (spots: { at: V3; t: number }[]): Rig => (ctx) => {
  const mat = new THREE.MeshBasicMaterial({ color: "#8e6a45", transparent: true, opacity: 0.8 });
  const ms = spots.map((s) => { const m = new THREE.Mesh(new THREE.RingGeometry(0.36, 0.46, 32), mat); m.rotation.x = -Math.PI / 2; m.position.set(s.at[0], 0.02, s.at[2]); ctx.root.add(m); return m; });
  return (t) => ms.forEach((m, i) => { m.visible = t >= spots[i].t; });
};
/** dust specks resting on the bronze (macro shield at the origin, radius 0.36) that start to hop and shiver at t0 */
const shiver = (t0: number): Rig => (ctx) => {
  const mat = new THREE.MeshBasicMaterial({ color: "#5b4030" });
  const specks = Array.from({ length: 70 }, (_, i) => {
    const a = i * 2.39996, r = 0.06 + 0.26 * Math.sqrt((i + 0.5) / 70);
    const m = new THREE.Mesh(new THREE.SphereGeometry(0.004 + (i % 4) * 0.002, 6, 4), mat);
    m.position.set(Math.cos(a) * r, 0.045 - r * 0.06, Math.sin(a) * r); ctx.root.add(m); return { m, y: m.position.y, x: m.position.x, z: m.position.z, ph: i * 1.7 };
  });
  return (t) => { const k = t >= t0 ? Math.min(1, (t - t0) / 0.4) : 0; const f = Math.floor(t * 30);
    for (const s of specks) { const j = Math.sin(f * 2.1 + s.ph); s.m.position.set(s.x + k * 0.006 * j, s.y + k * 0.012 * Math.abs(Math.sin(f * 1.3 + s.ph)), s.z + k * 0.006 * Math.cos(f * 1.7 + s.ph)); } };
};
/** a label that fades in and out at fixed times */
const label = (text: string, at: V3, t0: number, t1: number, h = 0.12): Rig => (ctx) => {
  const s = tagSprite(text, h); s.position.set(...at); ctx.root.add(s);
  const mat = (s as THREE.Sprite).material as THREE.SpriteMaterial;
  return (t) => { const o = sm((t - t0) / 0.2) * (1 - sm((t - t1) / 0.2)); s.visible = o > 0.01; mat.opacity = o; };
};

export function buildStory(T: Timing): BarcaStory {
  const DAY = mixKey("day", "night", 0.12), GOLD = mixKey("golden", "night", 0.1);
  const words = T.words as Word[];
  const w = (word: string, after = -1, n = 1) => wordT(words, word, n, after);
  const END = words[words.length - 1].end + 0.4;
  const groups: GroupSpec[] = [];

  // ---- word anchors (Kokoro timings)
  const tGuards = w("The", 4.5), tCracked = w("cracked"), tIts = w("It's"), tWhats = w("what's"), tBarca = w("Barca,");
  const tPersianArmy = w("and", tWhats), tFor = w("For"), tWalls = w("walls,", tFor), tHold = w("and", tWalls), tBut = w("But"), tGoHome = w("and", tBut);
  const tSo = w("So"), tHe = w("He"), tThen = w("then"), tLost = w('"Lost'), tEnemy = w('"The', tLost), tDays = w("For", tLost);
  const tJust = w("Just"), tThen2 = w("Then,", tJust), tSets2 = w("he", tThen2), tRings = w("rings,"), tDust = w("and", tRings);
  const tShiver = w("starts", tRings), tYou = w("You"), tAlso = w("they", tYou), tOver = w("Over"), tBut2 = w("But", tOver);
  const tEvery = w("every", tBut2), tRing = w("ring", tEvery), tSo2 = w("So", tEvery), tDefenders = w("the", w("rang,"));
  const tBroke = w("broke"), tAn = w("An", tBroke), tAnd3 = w("and", w("secret,")), tHeard = w("heard");

  // ---- cast and places
  const SM0: V3 = [-4, 0, -5.4];                                     // the hook spot
  const G1: V3 = [-2.6, WALL.h, -0.75], G2: V3 = [-1.4, WALL.h, -0.8];
  const SPOT: V3 = [-6.6, 0, -3.0];                                  // where it rings, by the tower
  const smith = (face: unknown, extra: Record<string, unknown> = {}) => ({ costume: "smith", seed: 3, face, ...extra });

  ROOM = CITY;
  // ================= 1a hook, "With an army outside the walls,": the Persian army massed at Barca's wall, ladders up, the
  // ram at the gate, smoke (panel rounds 1-2: "no army visible" on a static wall); then 1b the smith, close
  const tCity = w("city's") - 0.15;
  ROOM = null;
  {
    const t0 = 0, t1 = tCity;
    const A: V3[] = [[10.8, 0, 8.6], [12.0, 0, 9.0], [11.4, 0, 13.9]];
    groups.push({ sun: "auto", id: "army", place: "outside", t0, t1, xfade: 0, set: () => barcaSet(), lens: { cInf: 8 }, light: GOLD,
      alive: [[t0, t1]],                                                // the camp smoke rising behind them
      cam: ((k0: CamKey): CamKey[] => [{ ...k0, drift: 0.6 }, { ...k0, t: t1, glide: 1.6, drift: 0.6,
        pos: k0.pos.map((v, j) => k0.look[j] + (v - k0.look[j]) * 0.78) as V3, look: [k0.look[0], k0.look[1] + 0.6, k0.look[2] - 1.5] }])(cK(0, [A[2]], "medium", 12, -8, 50)),   // a push and tilt toward the gate (v14's hook read as still)   // low behind the front rank: the soldiers big, the wall, ladders and gate looming over them
      people: [...A.map((p, i): PersonSpec => ({ id: `a${i}`, at: () => p, faceTo: () => [p[0], 0, 0],
        props: () => ({ costume: i % 2 ? "persian2" : "persian", seed: 90 + i, face: i === 0 ? "sly" : "furious", item: i % 3 === 1 ? "spade" : "none",
          pose: [{ t: 0, v: i % 2 ? "armsUp" : "point" }, { t: 0.5 + i * 0.13, v: i % 2 ? "point" : "armsUp" }, { t: 1.1 + i * 0.11, v: i % 2 ? "armsUp" : "point" }] }) })),
        // the army behind the front rank (round-2 craft: "the army as tiny distant tents"): ranks of Persians facing the wall
        ...crowd("pa", [10.0, 16.5, 14.0, 22.5], 9, { costumes: ["persian", "persian2"], faces: ["furious", "frown", "focus", "sly"], poses: ["armsUp", "point", "hold", "stand"], face: [12, 0, 0], seed: 41 }),],
      rigs: [(ctx) => { const sm = [-9, 2, 16].map((x, i) => { const r = new Rising(10, "smoke", 3.2, 60 + i); r.group.position.set(x, 2, 18 + i * 3); ctx.root.add(r.group); return r; }); return (t) => sm.forEach((r) => r.update(t, 1, 1.0, 0.8, 16)); }] });
  }
  ROOM = CITY;
  {
    const t0 = tCity, t1 = tGuards;
    const faces = faceTrack(words, "focus", [{ word: "spent", face: "puzzled" }, { word: "dirt.", face: "focus" }], t0);
    const down = w("laying") + 0.4;                                  // the shield leaves his hands and lies in the dirt
    groups.push({ sun: "auto", id: "hook", place: "inside", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: GOLD,
      cam: [cK(t0, [SM0], "close", 196, 2, 36), cK(w("laying"), [SM0], "close", 160, 12, 36)],
      people: [{ id: "smith", at: () => SM0, faceTo: () => [SM0[0] + 1, 0, SM0[2]], props: (t) => smith(faces, { crouch: t < down ? 0.3 : 1, pose: t < down - 0.1 ? "hold" : "push", item: t < down ? "shield" : "none" }) }],
      rigs: [groundShield([SM0[0] + 0.85, 0.01, SM0[2] + 0.1], (t) => t >= down), debris([{ at: [SM0[0] + 0.85, 0.05, SM0[2] + 0.1], t: down, n: 14, kind: "shard", size: 0.03, floorY: 0.02, up: 1.2 }])] });
  }
  // ================= 2 the guards on the wall laugh down at him
  {
    const t0 = tGuards, t1 = tIts;
    const f1 = faceTrack(words, "sly", [{ word: "cracked", face: "cackle", react: [{ face: "squeeze", frames: 2 }] }], t0);
    const f2 = faceTrack(words, "deadpan", [{ word: "cracked", face: "grin", lead: -6 }], t0);
    const tRev = tCracked - 0.25;
    groups.push({ sun: "auto", id: "doubt", place: "walk", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: GOLD,
      cam: [cK(t0, [G1, G2], "medium", 196, 6, 36), { ...cK(t1 - 0.2, [G1, G2], "medium", 218, 0, 36), glide: 1.6 }],   // a slow orbit along the walk
      people: [
        { id: "g1", at: () => G1, faceTo: () => SM0, props: () => ({ costume: "hoplite", seed: 7, face: f1, pose: poseTrack(words, "hips", [["cracked", "point"]], t0) }) },
        { id: "g2", at: () => G2, faceTo: () => SM0, props: () => ({ costume: "hoplite2", seed: 9, face: f2, pose: "laugh" }) },
        // the rest of the watch along the walk, both sides of the two guards
        ...crowd("w", [-9.5, -1.0, -5.0, -0.5], 4, { costumes: ["hoplite", "hoplite2"], faces: ["focus", "frown", "deadpan"], poses: ["hold", "stand", "hips"], face: [0, 7, 8], seed: 7, y: WALL.h, spacing: 1.1 }),
        ...crowd("w2", [1.2, -1.0, 6.0, -0.5], 4, { costumes: ["hoplite", "hoplite2"], faces: ["focus", "grin", "deadpan"], poses: ["hold", "point", "stand"], face: [0, 7, 8], seed: 8, y: WALL.h, spacing: 1.1 })],
      rigs: [] });
    ROOM = null;
  }
  // ================= 3 the map: about 2,500 years ago, Barca, in what's now Libya
  {
    const t0 = tIts, t1 = tPersianArmy;
    groups.push({ sun: "auto", id: "map", place: "map", insert: true, t0, t1, xfade: 0.6,
      set: () => mapSet({ places: [{ name: "", u: 0.36, v: 0.4 }, { name: "", u: 0.42, v: 0.74 }], route: [[0.98, 0.72], [0.78, 0.62], [0.56, 0.52], [0.39, 0.43]], seed: 72 }),
      light: GOLD,
      // a slow sideways pan with no push (quiet frames without zoom: v4 measured 91 % quiet zoom against <= 88)
      alive: [[t0 + 0.1, tBarca - 0.1]],
      // round 2 (visible-change gate: v14's map window 9.7-12.8 s read as still): a slow push toward Barca with the route
      cam: [{ ...fit(t0, [[-1.7, 0.8, -1.2, 1.7, 0.85, 1.2]], 90, 72, 40, { b: 0.06, t: 0.06, x: 0.02 }), drift: 1 }, { ...fit(tWhats, [[-1.4, 0.8, -1.1, 1.7, 0.85, 1.2]], 96, 72, 40, { b: 0.06, t: 0.06, x: 0.02 }), drift: 0 }],
      people: [], rigs: [routeRig(t0 + 0.1, tBarca - 0.1, [tBarca, w("Libya,")]), label("BARCA", [(0.36 - 0.5) * 3.4, 1.15, (0.4 - 0.5) * 2.4 - 0.15], tBarca, t1 + 1, 0.24), label("ABOUT 2,500 YEARS AGO", [-1.3, 1.1, 0.3], t0 + 0.1, tBarca, 0.2), label("LIBYA", [(0.42 - 0.5) * 3.4, 1.05, (0.74 - 0.5) * 2.4], w("Libya,"), t1 + 1, 0.22)], clouds: false });
  }
  // ================= 4 the Persian army has the city surrounded (establishing, high)
  {
    const t0 = tPersianArmy, t1 = tFor;
    groups.push({ sun: "auto", id: "camp", place: "camp", establishing: true, t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: DAY,
      cam: [fit(t0, [[-30, 0, -14, 40, 12, 70]], 162, 34, 44, { b: 0.3, t: 0.1 })],
      people: [], rigs: [] });
  }
  // ================= 5 for months they hammer the walls (the ram, the ladders), and the walls hold
  {
    const t0 = tFor, t1 = tBut;
    const P: V3[] = [[14.2, 0, 9.6], [9.6, 0, 8.4], [4.4, 0, 6.2], [-0.8, 0, 6.0]];
    const D: V3 = [3.2, WALL.h, 0.4];
    const pf = faceTrack(words, "furious", [], t0);
    const df = faceTrack(words, "grimace", [{ word: "hold.", face: "grin" }], t0);
    groups.push({ sun: "auto", id: "assault", place: "gate", t0, t1: tHold, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: DAY,
      cam: [cK(t0, [P[0]], "medium", 56, 8, 40)],   // the soldier in front, the ram and the gate behind him
      people: [
        ...P.slice(0, 2).map((p, i): PersonSpec => ({ id: `p${i}`, at: () => p, faceTo: () => [p[0], 0, 0], props: () => ({ costume: i % 2 ? "persian2" : "persian", seed: 20 + i, face: pf, pose: i < 2 ? "push" : "armsUp" }) })),
      ],
      rigs: [
        (ctx) => { const ram = ctx.set.extra.ram as THREE.Object3D; return (t) => { const k = (t - t0) / 0.75; ram.position.z = 5.4 - 0.5 * Math.max(0, Math.sin(Math.max(0, k) * Math.PI)) * (k < 3 ? 1 : 0); }; },
        burst([{ at: [WALL.gateX, 2.2, 1.2], t: w("hammer"), size: 1.4 }, { at: [WALL.gateX, 2.2, 1.2], t: tWalls, size: 1.2 }]),
        debris([{ at: [WALL.gateX, 2.4, 1.2], t: w("hammer"), n: 24, kind: "splinter", floorY: 0.05 }, { at: [WALL.gateX, 2.4, 1.2], t: tWalls, n: 20, kind: "splinter", floorY: 0.05 }])] });
    // ... and the walls hold: a defender on the walk shoves a ladder off (its own shot, from the walk)
    groups.push({ sun: "auto", id: "hold", place: "walk-out", t0: tHold, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: DAY,
      cam: [cK(tHold, [D], "medium", 150, 6, 38)],
      people: [{ id: "def", at: () => D, faceTo: () => [3, 0, 6], props: () => ({ costume: "hoplite", seed: 7, face: df, pose: poseTrack(words, "push", [["hold.", "armsUp"]], t0) }) }],
      rigs: [] });
  }
  // ================= 6 the Persian commander does not give up and does not go home
  {
    const t0 = tBut, t1 = tSo;
    const L = CAMP.lord as V3;
    groups.push({ sun: "auto", id: "lord", place: "camp", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: lightArc([[t0, DAY], [tGoHome, GOLD, 0.6]]),
      cam: [{ ...cK(t0, [L], "close", 186, 6, 36), drift: 0.3 }],
      people: [{ id: "lord", at: () => L, faceTo: () => [L[0], 0, 0], props: () => ({ costume: "persianLord", seed: 31, face: faceTrack(words, "smug", [{ word: "home.", face: "sly" }], t0), pose: "hips" }) },
        ...[[0.1, 6.5], [0.5, 8.5], [-0.1, 10.5]].map(([dx, dz], i): PersonSpec => ({ id: `ps${i}`, at: () => [L[0] + dx, 0, L[2] + dz], faceTo: () => [L[0], 0, 0], props: () => ({ costume: i % 2 ? "persian2" : "persian", seed: 80 + i, face: "furious", item: "spade", pose: "hold" }) }))],
      rigs: [(ctx) => { const sm1 = new Rising(10, "smoke", 2.6, 40); sm1.group.position.set(L[0] + 5, 1, L[2] + 2); ctx.root.add(sm1.group); return (t) => sm1.update(t, 1, 1.0, 0.8, 14); }] });
  }
  ROOM = CITY;
  // ================= 7 the smith walks the inside of the wall: down, kneel, listen, move on, again
  {
    const t0 = tSo, t1 = tLost;
    const x = (t: number) => -19 + 3 * clamp01((t - t0) / (tHe - t0 - 0.2)) + 1.6 * clamp01((t - tThen - 0.3) / 0.8);   // the camera widens first, then he moves on
    const at = (t: number): V3 => [x(t), 0, -3.0];
    const kneel = (t: number) => (t >= tHe + 0.4 && t < tThen) || t >= w("again.") - 0.5 ? 1 : 0;
    const faces = faceTrack(words, "focus", [{ word: "listens,", face: "puzzled" }, { word: "again.", face: "focus" }], t0);
    groups.push({ sun: "auto", id: "walk", place: "inside", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: DAY,
      cam: [cK(t0, [at(t0), at(tHe)], "medium", 160, 8, 40), cK(tHe + 0.2, [at(tHe + 0.4)], "close", 196, 8, 36), { ...fit(tThen, [personBox(at(tThen)), personBox(at(t1)), [-19.8, 0, -3.6, -12.8, 0.1, -2.4]], 172, 26, 40, { b: 0.12, t: 0.1, x: 0.1 }), glide: 0.6, drift: 0.15 }],   // fit, not castKey: castKey zooms to a head size and lets a walker leave
      people: [{ id: "smith", at, faceTo: (t) => [x(t) + 1, 0, -3], props: (t) => smith(faces, { crouch: kneel(t), pose: "hold", item: kneel(t) ? "none" : "shield", walk: kneel(t) ? 0 : 1 }) }],
      rigs: [groundShield([-15.2, 0.01, -2.9], (t) => t >= tHe + 0.5 && t < tThen), groundShield([-13.5, 0.01, -2.9], (t) => t >= w("again.") - 0.3),
        dustRings([{ at: [-19.5, 0, -2.9], t: 0 }, { at: [-17.4, 0, -2.9], t: 0 }, { at: [-15.2, 0, -2.9], t: tThen }])] });
  }
  // ================= 8 "Lost something?" a guard laughs. "The enemy's out there, not down there."
  {
    const t0 = tLost, t1 = tDays;
    const SM: V3 = [-14.4, 0, -3.0];
    const f1 = faceTrack(words, "smug", [{ word: "laughs.", face: "cackle", react: [{ face: "squeeze", frames: 2 }] }, { word: '"The', after: tLost, face: "sly" }], t0);
    const GJ: V3 = [-16.6, WALL.h, -0.75], tRev = tEnemy - 0.15;
    const gPose = [{ t: t0, v: "laugh" }, { t: tEnemy - 0.07, v: "point" }, { t: w("down", tEnemy) - 0.07, v: "push" }];
    ROOM = CITY;
    groups.push({ sun: "auto", id: "jeer", place: "walk", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: DAY,
      cam: [cK(t0, [GJ], "close", 200, -6, 36), { ...cK(t1 - 0.2, [GJ], "close", 176, -4, 36), glide: 1.6 }],
      people: [{ id: "g1", at: () => GJ, faceTo: () => SM, props: () => ({ costume: "hoplite", seed: 7, face: f1, quote: [[t0, t0 + 0.9], [tEnemy, t1 - 0.1]], pose: gPose }) }],
      rigs: [] });
  }
  // ================= 9 for days, nothing: the DAY tally on the wall, the light turning day after day
  {
    const t0 = tDays, t1 = tJust;
    const xs = [-10.6, -9.6, -8.6];
    const k = (t: number) => Math.min(2, Math.floor(((t - t0) / (t1 - t0)) * 3));
    const at = (t: number): V3 => [xs[k(t)], 0, -3.0];
    groups.push({ sun: "auto", id: "days", place: "inside", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: lightArc([[t0, DAY], [t0 + 0.4, GOLD, 0.3], [t0 + 0.8, DAY, 0.3]]),
      cam: [cK(t0, xs.map((x): V3 => [x, 0, -3]), "medium", 196, 10, 40, 1, [[-11.4, 1.6, -1.6, -7.8, 3.2, -1.5]])],
      people: [{ id: "smith", at, faceTo: () => [0, 0, -3], props: () => smith(faceTrack(words, "worried", [{ word: "nothing.", face: "deadpan" }], t0), { crouch: 1, pose: "hold" }) }],
      rigs: [counter({ at: [-9.6, 2.4, -1.47], rotY: Math.PI, w: 1.5, digits: 1, from: 3, to: 9, t0, t1, steps: [[t0, 3], [t0 + 0.45, 5], [t0 + 0.9, 7], [w("nothing."), 9]], label: "DAY" }),
        (ctx) => { const s = shieldMesh(0.42); ctx.root.add(s); return (t) => { const p = at(t); s.position.set(p[0] + 0.85, 0.01, -2.9); }; }] });
  }
  // ================= 10 just a dull thud (macro: a puff of dust, no rings)
  {
    const t0 = tJust, t1 = tThen2;
    groups.push({ sun: "auto", id: "thud", place: "macro", insert: true, t0, t1, xfade: 0.6, set: () => shieldMacroSet(), light: GOLD, lens: { cInf: 20 },
      cam: [fit(t0, [[-0.4, 0, -0.4, 0.4, 0.1, 0.4]], 20, 32, 34, { b: 0.4, t: 0.18 })],
      people: [], rigs: [(ctx) => { const s = ctx.set.extra.shield as THREE.Object3D; return (t) => { const u = clamp01((t - t0) / 0.25); s.position.y = 0.12 * (1 - u * u); }; },
        debris([{ at: [0, 0.03, 0.2], t: w("thud,"), n: 18, kind: "shard", size: 0.012, speed: 0.4, floorY: 0.01, up: 0.6 }])] });
  }
  // ================= 11 then, at one spot by the wall (by the tower, dusk)
  {
    const t0 = tThen2, t1 = tSets2;
    groups.push({ sun: "auto", id: "spot", place: "tower", t0, t1, xfade: 0.6, set: () => barcaSet(), lens: { cInf: 8 }, light: GOLD,
      cam: [cK(t0, [SPOT], "close", 214, 10, 36, 1, [])],
      people: [{ id: "smith", at: () => SPOT, faceTo: () => [SPOT[0] + 1, 0, SPOT[2]], props: () => smith("focus", { crouch: 1, pose: "hold" }) }],
      rigs: [groundShield([SPOT[0] + 0.85, 0.01, SPOT[2] + 0.1])] });
  }
  // ================= 12 it rings, and the dust on the bronze starts to shiver (macro)
  {
    const t0 = tSets2, t1 = tShiver;
    const hop = Array.from({ length: 10 }, (_, i) => ({ at: [(i % 5 - 2) * 0.09, 0.06, (Math.floor(i / 5) - 0.5) * 0.12] as V3, t: tDust + (i % 5) * 0.12, n: 6, kind: "shard" as const, size: 0.01, speed: 0.25, floorY: 0.05, up: 0.4, seed: i }));
    groups.push({ sun: "auto", id: "ring", place: "macro", insert: true, alive: [[tDust, t1]], t0, t1, xfade: 0.6, set: () => shieldMacroSet(), light: lightArc([[t0, GOLD]], [{ kind: "flash", t: tRings, frames: 2 }]), lens: { cInf: 20 },
      cam: [fit(t0, [[-0.4, 0, -0.4, 0.4, 0.1, 0.4]], -24, 34, 34, { b: 0.4, t: 0.18 })],
      people: [], rigs: [burst([{ at: [0, 0.08, 0], t: tRings, size: 0.9 }, { at: [0, 0.08, 0], t: tRings + 0.35, size: 0.7 }]),
        glints([{ at: [0.3, 0.06, 0.1], t: tRings + 0.05, size: 0.06 }, { at: [-0.2, 0.06, -0.2], t: tRings + 0.3, size: 0.05 }]), debris(hop), shiver(tDust)] });
  }
  // ================= 13 the smith's face: he heard it
  {
    const t0 = tShiver, t1 = tYou;
    groups.push({ sun: "auto", id: "face", place: "tower", t0, t1, xfade: 0, set: () => barcaSet(), lens: { cInf: 8 }, light: GOLD,
      cam: [cK(t0, [SPOT], "close", 180, 4, 32)],
      people: [{ id: "smith", at: () => SPOT, faceTo: () => [SPOT[0] + 1, 0, SPOT[2]], props: () => smith(faceTrack(words, "focus", [{ word: "shiver.", face: "stunned", react: [{ face: "blank", frames: 2 }] }], t0), { crouch: 1, pose: "push", marks: [markAt(words, "shiver.", "sweat")] }) }],
      rigs: [groundShield([SPOT[0] + 0.85, 0.01, SPOT[2] + 0.1])] });
  }
  ROOM = null;
  // ================= 14-15 the cross-section: they were digging under the walls; solid thuds, hollow rings
  const sectionCast = (t0: number): PersonSpec[] => [0, 1, 2].map((i): PersonSpec => {
    const x = SEC.cav.x - 1.6 + i * 1.6, floor = SEC.cav.y - SEC.cav.h;
    return { id: `dig${i}`, scale: 0.8, at: () => [x, floor, -0.7], faceTo: () => [x - 1, floor, -0.7],
      props: (t) => ({ costume: "digger", seed: 40 + i, face: "focus", item: "pick", pose: Math.floor((t - t0) / 0.3 + i) % 2 ? "strike" : "strikeUp" }) };
  });
  /** chips flying off the tunnel face as the picks strike */
  const chips = (t0: number, t1: number): Rig => debris(Array.from({ length: Math.max(1, Math.floor((t1 - t0) / 0.6)) }, (_, k) => ({ at: [SEC.cav.x - SEC.cav.w / 2 + 0.6 + (k % 3) * 1.6, SEC.cav.y - SEC.cav.h + 1.2, -0.6] as V3, t: t0 + 0.2 + k * 0.6, n: 10, kind: "shard" as const, size: 0.04, floorY: SEC.cav.y - SEC.cav.h + 0.05, up: 0.8, seed: k })));
  {
    const t0 = tYou, t1 = tOver;
    groups.push({ sun: "auto", id: "under", place: "section", insert: true, t0, t1, xfade: 0.6, set: () => sectionSet(), lens: { cInf: 3 }, light: lightArc([[t0, "explain"]]),
      cam: [fit(t0, [[-3.0, -5.2, -1, 6.0, 4.2, 0.4]], 0, 8, 40, { b: 0.36, t: 0.06, x: 0.02 }), fit(tAlso, [[-0.6, SEC.cav.y - SEC.cav.h, -1, 5.0, SEC.cav.y + 0.6, 0.2]], -26, 4, 32, { b: 0.42, t: 0.18 })],
      people: sectionCast(t0), clouds: false,
      rigs: [chips(t0, t1), (ctx) => { const lamp = ctx.set.extra.lamp as THREE.Mesh; return (t) => { lamp.scale.setScalar(1 + 0.15 * Math.sin(Math.floor(t * 12) * 1.7)); }; }] });
  }
  {
    const t0 = tOver, t1 = tSo2;
    const pickTip: V3 = [SEC.cav.x, SEC.cav.y - 0.6, 0.1];
    const waves = [0, 1, 2, 3].map((k) => ({ at: [SEC.shieldHollow, SEC.cav.y + (0 - SEC.cav.y) * (k / 3), 0.2] as V3, t: tEvery + 0.35 + k * 0.12, size: 0.6 + k * 0.1 }));
    groups.push({ sun: "auto", id: "mechanism", place: "section", insert: true, t0, t1, xfade: 0, set: () => sectionSet(), lens: { cInf: 3 }, light: "explain",
      cam: [fit(t0, [[SEC.shieldSolid - 1.8, -1.6, -1, SEC.shieldSolid + 1.8, 1.6, 0.8]], 0, 22, 38, { b: 0.5, t: 0.1 }),
        fit(tBut2 - 0.5, [[SEC.shieldSolid - 1.6, -1.4, -1, SEC.shieldSolid + 1.6, 1.6, 0.8]], 8, 26, 36, { b: 0.5, t: 0.1 }),   // a slow push on the solid side (the drift toward the hollow side pushed the label out)
        { ...fit(tBut2, [[SEC.shieldHollow - 1.6, SEC.cav.y - SEC.cav.h, -1, SEC.shieldHollow + 1.6, 1.6, 0.8]], 0, 14, 40, { b: 0.42, t: 0.08 }), glide: 1.0 },
        { ...fit(tEvery, [[SEC.shieldHollow - 1.6, SEC.cav.y - SEC.cav.h, -1, SEC.shieldHollow + 1.6, 1.7, 0.8]], 30, 16, 38, { b: 0.58, t: 0.06, x: 0.12 }), drift: 0.3 }],
      people: sectionCast(t0).map((p) => ({ ...p, visible: (t: number) => t >= tBut2 - 0.2 })), clouds: false,
      keepInFrame: (t) => [...(t < tBut2 + 0.6 && t > t0 + 0.3 ? [[SEC.shieldSolid - 0.9, 1.1, 0.65, SEC.shieldSolid + 0.9, 1.4, 0.75] as Box] : []), ...(t > tBut2 + 1.0 ? [[SEC.shieldHollow - 0.9, 1.1, 0.65, SEC.shieldHollow + 0.9, 1.4, 0.75] as Box] : [])],
      rigs: [label("SOLID GROUND", [SEC.shieldSolid, 1.25, 0.7], t0 + 0.1, tBut2 + 0.6, 0.55), label("HOLLOW TUNNEL", [SEC.shieldHollow, 1.25, 0.7], tBut2 + 0.2, t1, 0.55),
        debris([{ at: [SEC.shieldSolid, 0.2, -0.4], t: w("thuds."), n: 12, kind: "shard", size: 0.03, floorY: 0.12, up: 0.5 }]),
        burst([{ at: pickTip, t: w("pick"), size: 0.7 }, ...waves, { at: [SEC.shieldHollow, 0.25, -0.4], t: tRing, size: 1.1 }, { at: [SEC.shieldHollow, 0.25, -0.4], t: w("bell."), size: 1.3 }]),
        glints([{ at: [SEC.shieldHollow + 0.3, 0.3, -0.2], t: tRing + 0.05, size: 0.12 }])] });
  }
  ROOM = CITY;
  // ================= 16 so wherever it rang, the defenders dig (night, torches)
  {
    const t0 = tSo2, t1 = tDefenders;
    const D: V3[] = [[SPOT[0] - 0.4, 0, SPOT[2] - 1.3], [SPOT[0] + 1.9, 0, SPOT[2] - 1.0]];
    groups.push({ sun: "auto", id: "dig", place: "tower", t0, t1, xfade: 0.6, set: () => barcaSet({ night: true }), lens: { cInf: 8 }, light: "night",
      cam: [{ ...fit(t0, [personBox(SPOT), ...D.map((d) => personBox(d))], 196, 14, 40, { b: 0.1, t: 0.12, x: 0.14 }), drift: 0.3 }],
      people: [{ id: "smith", at: () => SPOT, faceTo: () => [SPOT[0] + 1, 0, SPOT[2]], props: () => smith("focus", { pose: "point" }) },
        ...D.map((p, i): PersonSpec => ({ id: `d${i}`, at: () => p, faceTo: () => [SPOT[0] + 0.85, 0, SPOT[2]], props: (t) => ({ costume: i ? "hoplite2" : "hoplite", seed: 50 + i, face: "furious", item: "spade", pose: Math.floor((t - t0) * 2.5 + i) % 2 ? "strike" : "strikeUp" }) }))],
      rigs: [dustRings([{ at: [SPOT[0] + 0.85, 0, SPOT[2] + 0.1], t: 0 }])] });
  }
  ROOM = null;
  // ================= 17 they dug straight down and broke into the tunnel from above (section)
  {
    const t0 = tDefenders, t1 = tAn;
    const floor = SEC.cav.y;
    const depth = (t: number) => (floor - 0.05) * clamp01((t - t0) / (tBroke - t0)) - (t >= tBroke ? 0.3 : 0);
    const D: [number, number][] = [[-0.25, 0], [0.3, 0.2]];
    groups.push({ sun: "auto", id: "break", place: "section", insert: true, t0, t1, xfade: 0.6, set: () => sectionSet(), lens: { cInf: 3 }, light: lightArc([[t0, "explain"]], [{ kind: "flash", t: tBroke, frames: 2 }]),
      cam: [fit(t0, [[SEC.shieldHollow - 2.6, SEC.cav.y - SEC.cav.h, -1, SEC.shieldHollow + 2.6, 1.6, 0.4]], 0, 6, 40, { b: 0.5, t: 0.08 })],
      people: [...sectionCast(t0).map((p) => ({ ...p, props: (t: number) => ({ ...p.props(t), face: t >= tBroke ? "terrified" : "focus", pose: t >= tBroke ? "armsUp" : p.props(t).pose }) })),
        ...D.map(([dx, dz], i): PersonSpec => ({ id: `cm${i}`, scale: 0.8, at: (t) => [SEC.shieldHollow + dx, Math.min(0.12, depth(t) - 0.0 + (i ? 0.35 : 0)), 0.25 + dz], faceTo: () => [SEC.shieldHollow, -5, 0],
          props: (t) => ({ costume: i ? "hoplite2" : "hoplite", seed: 60 + i, face: t >= tBroke ? "furious" : "focus", item: "spade", pose: Math.floor((t - t0) * 2.5 + i) % 2 ? "strike" : "strikeUp" }) }))],
      clouds: false,
      rigs: [(ctx) => { const shaft = ctx.set.extra.shaft as THREE.Mesh, sh = ctx.set.extra.shieldHollow as THREE.Object3D; return (t) => {
          const d = Math.max(0.05, -depth(t)); shaft.visible = t >= t0 + 0.1; shaft.scale.set(1, d, 1); shaft.position.y = -d / 2; sh.visible = t < t0 + 0.1; }; },
        debris([{ at: [SEC.shieldHollow, SEC.cav.y - 0.1, 0.1], t: tBroke, n: 40, kind: "shard", size: 0.05, floorY: SEC.cav.y - SEC.cav.h + 0.05 }]),
        burst([{ at: [SEC.shieldHollow, SEC.cav.y - 0.2, 0.2], t: tBroke, size: 1.4 }])] });
  }
  // ================= 18 an army spent months digging in secret (the camp at night, establishing)
  {
    const t0 = tAn, t1 = tAnd3;
    groups.push({ sun: "auto", id: "night", place: "camp", establishing: true, t0, t1, xfade: 0.6, set: () => barcaSet({ night: true }), lens: { cInf: 8 }, light: "night",
      cam: [fit(t0, [[-30, 0, 4, 34, 10, 70]], 196, 22, 44, { b: 0.3, t: 0.1 })],
      people: [], rigs: [] });
  }
  // ================= 19 and a shield lying in the dirt heard every swing: the cut once more, from the picks in the
  // tunnel up to the shield on the surface, ringing on every swing (panel round 2: "the payoff is told, not shown")
  {
    const t0 = tAnd3, t1 = END;
    const rings = ["heard", "every", "swing."].map((x) => w(x, tAnd3));
    groups.push({ sun: "auto", id: "last", place: "section-end", insert: true, t0, t1, xfade: 0.6, set: () => sectionSet(), lens: { cInf: 3 }, light: "explain",
      cam: [fit(t0, [[SEC.shieldHollow - 1.8, SEC.cav.y - SEC.cav.h, -1, SEC.shieldHollow + 1.8, SEC.cav.y + 0.4, 0.4]], 8, 4, 38, { b: 0.42, t: 0.12 }),
        { ...fit(rings[0], [[SEC.shieldHollow - 2.4, SEC.cav.y - SEC.cav.h, -1, SEC.shieldHollow + 2.4, 1.2, 0.6]], -6, 28, 38, { b: 0.42, t: 0.08, x: 0.06 }), glide: 1.2 }],
      people: sectionCast(t0), clouds: false,
      rigs: [chips(t0, t1), burst(rings.flatMap((t) => [{ at: [SEC.cav.x, SEC.cav.y - 0.6, 0.1] as V3, t: t - 0.12, size: 0.6 }, { at: [SEC.shieldHollow, 0.3, -0.4] as V3, t, size: 1.2 }])),
        glints(rings.map((t, k) => ({ at: [SEC.shieldHollow + 0.3 - k * 0.2, 0.32, -0.2] as V3, t: t + 0.04, size: 0.12 })))] });
  }
  return { groups };
}
