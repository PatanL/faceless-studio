// story-myeongnyang (our own code): Korea, 1597. Ordered to give up the navy, Admiral Yi takes his last thirteen ships
// to the Myeongnyang strait and fights the Japanese fleet of 133; the strait's river-like current, which turns four
// times a day, carries the Japanese into a gap where only a few can reach him, then (historians think) turns and
// shoves them back into each other. Shot groups are word-anchored on the Kokoro timings, following
// episodes/story-myeongnyang/shot_plan.md: castKey presets for people, light arcs, whips between places.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../kit/Stage";
import type { Timing } from "../kit/timing";
import { fit as fit0, tagSprite, setRoom, sm, personBox, type Box } from "../kit/framing";
import { castKey } from "../kit/castframe";
import type { CamKey } from "../kit/campath";
import { faceTrack, poseTrack, wordT, markAt, type Word } from "../kit/acting";
import { glints, burst, debris, counter } from "../kit/fx2";
import { lightArc, mixKey } from "../kit/lightarc";
import { PRESETS } from "../kit/presets";
import { Rising, Flame } from "../kit/fx";
import { straitSet, landH, currentRig, fleetRig, korean, japanese, koreanLine, japaneseFleet, onDeck, lanternGlows, courtSet, wreckRig, DECK_K, DECK_J, type Berth } from "./sets";

export type MyeongStory = { groups: GroupSpec[] };

let HOOK = "D";
/** the hook still check (three candidate first frames) picks a variant through the props */
export const setHook = (v: string) => { HOOK = v; };

const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
let ROOM: Box | null = null;
const fit = (...a: Parameters<typeof fit0>) => { setRoom(ROOM); const k = fit0(...a); setRoom(null); return k; };
const cK = (...a: Parameters<typeof castKey>) => { setRoom(ROOM); const k = castKey(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7] ?? [], a[8] ?? ROOM ?? undefined); setRoom(null); return { ...k, drift: a[2] === "wide" ? 0.3 : a[2] === "close" ? 0.5 : 0.4 }; };
/** a key toward the look point by k (k < 1 pushes in), with the look raised by dy */
/** a pair framed whole (castKey zooms pairs apart to the frame edges) */
const pair = (t: number, ps: V3[], az: number, el: number, fov = 40, drift = 0.3): CamKey => ({ ...fit(t, ps.map((p) => personBox(p)), az, el, fov, { b: 0.34, t: 0.16, x: 0.14 }), drift });
const push = (k0: CamKey, t: number, k: number, extra: Partial<CamKey> = {}): CamKey => ({ ...k0, t, pos: k0.pos.map((v, j) => k0.look[j] + (v - k0.look[j]) * k) as V3, ...extra });
/** a world label that pops in at t0 and out at t1 */
const label = (text: string, at: V3 | ((t: number) => V3), t0: number, t1: number, h = 1.2): Rig => (ctx) => {
  const s = tagSprite(text, h); ctx.root.add(s);
  const mat = (s as THREE.Sprite).material as THREE.SpriteMaterial;
  return (t) => { const p = typeof at === "function" ? at(t) : at; s.position.set(...p); const o = sm((t - t0) / 0.12) * (1 - sm((t - t1) / 0.12)); s.visible = o > 0.01; mat.opacity = o; };
};

export function buildStory(T: Timing): MyeongStory {
  const words = T.words as Word[];
  const w = (word: string, after = -1, n = 1) => wordT(words, word, n, after);
  const END = words[words.length - 1].end + 0.4;
  const groups: GroupSpec[] = [];
  const DUSK = mixKey("golden", "fire", 0.45);
  const DUSKL = mixKey("golden", "fire", 0.3);

  // ---- the fleets
  // Yi's thirteen: the flagship ahead, twelve in three rows of four behind it (a compact block at the west mouth)
  const KB: Berth[] = koreanLine();
  const FLAG = KB[0];
  const JB: Berth[] = japaneseFleet(84);
  const yiAt = (b: Berth, dx = 0): V3 => onDeck({ ...b, x: b.x + dx }, 6.6, 0, DECK_K);
  const YI = yiAt(FLAG);
  const yiProps = (face: unknown, extra: Record<string, unknown> = {}) => ({ costume: "yi", seed: 13, face, ...extra });

  // the current: phase (m moved, +x positive) and white-water amount; it runs west (-x) carrying the Japanese in,
  // goes slack ("the roaring stops"), then turns east (+x)
  const tStops = w("stops."), tTurned = w("turned,");
  const flowIn = (t: number) => -2.2 * t, flowOut = (t: number) => 2.4 * t;
  const westCur = currentRig(flowIn, () => 1);

  // ================= 1 the hook: Yi's thirteen at the mouth of the strait, facing the 133 pouring through the gap
  const tYi = w("Admiral"), tThirteen = w("thirteen"), tHundred = w("hundred"), tEven = w("Even");
  const japMove = (v = 0.9) => (t: number, b: Berth) => ({ dx: -v * t * (b.x < 140 ? 1 : 0.7) });
  {
    const t0 = 0, t1 = tThirteen - 0.15;
    const yiFace = faceTrack(words, "furious", [{ word: "Admiral", face: "focus" }], t0);
    const yiPose = poseTrack(words, "point", [["Admiral", "point"]], t0);
    const cam: CamKey[] = HOOK === "B"
      ? [{ ...cK(0, [YI], "medium", -58, 20, 54), drift: 0 }, { ...cK(t1, [YI], "medium", -52, 18, 54), glide: 1 }]
      : HOOK === "C"
      ? [{ t: 0, pos: [-112, 62, -64], look: [40, 0, 10], fov: 46, drift: 0.3 }, { t: t1, pos: [-104, 58, -60], look: [42, 0, 10], fov: 46, glide: 1 }]
      : HOOK === "A"
      ? [{ t: 0, pos: [-70, 62, -8], look: [60, 0, 2], fov: 46, drift: 0.3 }, { t: t1, pos: [-65, 58, -7], look: [62, 0, 2], fov: 46, glide: 1 }]
      // D (the pick of the hook check, with Yi brought into the foreground): behind Yi at the bow of his flagship, his
      // twelve in two columns ahead of him, the 133 filling the strait beyond
      : [{ t: 0, pos: [YI[0] - 8.0, 5.4, 0], look: [YI[0] - 0.16, 4.75, 0.73], fov: 52, drift: 0 }, { t: t1, pos: [YI[0] - 5.6, 5.2, 0.9], look: [YI[0] + 2.2, 4.75, 1.3], fov: 52, glide: 1 }];
    groups.push({ sun: "auto", id: "hook", place: "strait", t0, t1, xfade: 0, set: () => straitSet(), light: "golden", lens: { cInf: 4 },
      establishing: HOOK === "A" || HOOK === "C", cam, alive: [[0, t1]],
      people: [{ id: "yi", at: () => YI, faceTo: () => [YI[0] + 10, YI[1], YI[2]], props: () => yiProps(yiFace, { pose: yiPose }) },
        ...(HOOK === "D" ? [] : [[-2.2, 1.6], [-2.8, -1.8]]).map(([lx, lz], i): PersonSpec => ({ id: `ks${i}`, at: () => onDeck(FLAG, lx, lz, DECK_K), faceTo: () => [YI[0] + 10, DECK_K, YI[2]], props: () => ({ costume: "jsailor", seed: 20 + i, face: i ? "worried" : "grimace", pose: i ? "hold" : "stand" }) }))],
      rigs: [westCur, fleetRig((b) => korean(b.k === 0, HOOK === "D" ? b.k === 0 : true), KB), fleetRig((b) => japanese(b.k), JB, japMove()),
        label("13 SHIPS", HOOK === "D" ? [44, 8, 4] : [-6, 22, 0], -1, t1 + 1, HOOK === "D" ? 2.2 : 5), label("133 SHIPS", HOOK === "D" ? [190, 40, -8] : [150, 34, HOOK === "C" ? 30 : 0], -1, t1 + 1, HOOK === "D" ? 11 : 9)] });
  }
  // ================= hook candidates after the S-hook correction (frame 0 = Yi close, doing the odd act, >= 1/3 of the
  // frame height; the 13-vs-133 wide follows by 2-3 s). Stills only until the narration is locked: they replace group 1.
  if (HOOK.startsWith("H")) {
    const g0 = groups.shift()!;
    const t0 = 0, t1 = g0.t1;
    const Y = YI;
    if (HOOK === "H2") {
      // Yi kneeling at a low desk by lamplight, brush in hand, the king's sealed order unrolled beside his reply
      const D: V3 = onDeck(FLAG, 6.0, 0.0, DECK_K), P: V3 = [D[0] - 0.9, DECK_K, D[2] + 0.1];
      groups.unshift({ sun: "auto", id: "hook", place: "yi-night", t0, t1, xfade: 0, set: () => straitSet({ night: true }), light: "night", lens: { cInf: 7 }, alive: [[0, t1]],
        cam: [{ t: 0, pos: [P[0] + 2.6, DECK_K + 1.55, P[2] + 2.2], look: [P[0] + 0.25, DECK_K + 0.85, P[2] - 0.1], fov: 40, drift: 0 }, { t: t1, pos: [P[0] + 2.3, DECK_K + 1.5, P[2] + 1.95], look: [P[0] + 0.25, DECK_K + 0.85, P[2] - 0.1], fov: 40, glide: 1 }],
        people: [{ id: "yi", at: () => P, faceTo: () => D, props: (t) => yiProps(t < 1.2 ? "focus" : "furious", { kneel: 1, pose: Math.floor(t * 4) % 2 ? "reach" : "hold", item: "brush" }) }],
        rigs: [fleetRig((b) => korean(b.k === 0), KB), lanternGlows([[D[0] + 0.1, DECK_K + 0.95, D[2] - 0.55], ...KB.slice(1).map((b): V3 => [b.x + 3, DECK_K + 2, b.z])], 2.2), orderDesk(D)] });
    } else {
      // H1: low, Yi big at the bow, sword raised, the fleet pouring in behind him; H3: from above, the strait full of sails
      const low = HOOK === "H1";
      // the lens focuses at the look point: aim along the ray to the far target but put the look point at Yi's distance
      const aim = (pos: V3, far: V3, t: number, glide?: number): CamKey => { const d = [far[0] - pos[0], far[1] - pos[1], far[2] - pos[2]], n = Math.hypot(...d);
        const fd = Math.hypot(Y[0] - pos[0], Y[1] + 1.2 - pos[1], Y[2] - pos[2]); return { t, pos, look: d.map((v, j) => pos[j] + (v / n) * fd) as V3, fov: low ? 46 : 48, ...(glide ? { glide } : { drift: 0 }) }; };
      const cam: CamKey[] = low
        ? [aim([Y[0] - 4.6, Y[1] + 1.2, Y[2] + 1.9], [Y[0] + 40, Y[1] + 3.5, Y[2] - 9], 0), aim([Y[0] - 4.1, Y[1] + 1.15, Y[2] + 1.7], [Y[0] + 40, Y[1] + 3.3, Y[2] - 9], t1, 1)]
        : [aim([Y[0] - 4.0, Y[1] + 3.9, Y[2] + 1.2], [Y[0] + 36, Y[1] - 9.5, Y[2] - 3], 0), aim([Y[0] - 3.5, Y[1] + 3.6, Y[2] + 1.0], [Y[0] + 36, Y[1] - 9.0, Y[2] - 3], t1, 1)];
      groups.unshift({ ...g0, id: "hook", establishing: false, lens: { cInf: 5 }, cam, alive: [[0, t1]],
        people: [{ id: "yi", at: () => Y, faceTo: () => [Y[0] + 10, Y[1], Y[2]], props: (t) => yiProps(t < 0.6 ? "focus" : "furious", { pose: "holdHigh", item: "sword" }) }],
        rigs: [westCur, fleetRig((b) => korean(b.k === 0, b.k === 0), KB), fleetRig((b) => japanese(b.k), JB, japMove(2.5))] });
    }
  }
  // ================= 2 "...to fight a hundred and thirty-three": over a samurai's shoulder on the lead Japanese ship, the
  // whole fleet around him, the thin Korean line ahead; he laughs
  const LEAD = JB[1];
  {
    const t0 = tThirteen - 0.15, t1 = tEven;
    const S1 = onDeck(LEAD, 3.4, 0.5, DECK_J), S2 = onDeck(LEAD, 2.2, -0.6, DECK_J);
    groups.push({ sun: "auto", id: "armada", place: "jfleet", t0, t1, xfade: 0.6, set: () => straitSet(), light: "golden", lens: { cInf: 4 },
      cam: [pair(t0, [S1, S2], -62, 12, 46, 0), { ...pair(t1, [S1, S2], -44, 16, 50, 0), glide: 1.4 }],
      people: [{ id: "sam", at: () => S1, faceTo: () => [S1[0] - 10, S1[1], S1[2]], props: () => ({ costume: "samurai", seed: 31, face: faceTrack(words, "smug", [{ word: "hundred", face: "cackle", react: [{ face: "squeeze", frames: 2 }] }], t0), pose: poseTrack(words, "point", [["hundred", "laugh"]], t0) }) },
        { id: "ash", at: () => S2, faceTo: () => [S2[0] - 10, S2[1], S2[2]], props: () => ({ costume: "ashigaru", seed: 32, face: faceTrack(words, "grin", [{ word: "thirty-three.", face: "cackle" }], t0), pose: "armsUp" }) }],
      rigs: [westCur, fleetRig((b) => korean(b.k === 0), KB), fleetRig((b) => japanese(b.k), JB.filter((b) => b !== LEAD)), fleetRig((b) => japanese(b.k), [LEAD]),
        label("133", [LEAD.x + 40, 26, LEAD.z], tHundred, t1 + 1, 6)] });
  }
  // ================= 3 his own captains think he has lost his mind (on the next ship, Yi pointing at the bow beyond)
  const KC = KB[1];
  {
    const t0 = tEven, t1 = w("Korea's");
    const C1 = onDeck(KC, 1.4, 0.8, DECK_K), C2 = onDeck(KC, 0.6, -0.6, DECK_K);
    groups.push({ sun: "auto", id: "captains", place: "kdeck", t0, t1, xfade: 0.6, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [pair(t0, [C1, C2], -60, 6, 40, 0.5)],
      people: [
        { id: "c1", at: () => C1, faceTo: () => C2, props: () => ({ costume: "jcaptain", seed: 41, face: faceTrack(words, "worried", [{ word: "lost", face: "dizzy" }], t0), pose: poseTrack(words, "shrug", [["lost", "facepalm"]], t0), marks: [markAt(words, "lost", "sweat")] }) },
        { id: "c2", at: () => C2, faceTo: () => C1, props: () => ({ costume: "jcaptain2", seed: 42, face: faceTrack(words, "puzzled", [{ word: "mind.", face: "grimace" }], t0), pose: poseTrack(words, "point", [["mind.", "cheeks"]], t0) }) },
        { id: "yi", at: () => YI, faceTo: () => [YI[0] + 10, YI[1], YI[2]], props: () => yiProps("furious", { pose: "point" }) }],
      rigs: [westCur, fleetRig((b) => korean(b.k === 0), KB), fleetRig((b) => japanese(b.k), JB, japMove())] });
  }
  // ================= 4 Korea's navy wiped out: dusk, burning wrecks, the Japanese sailing past
  {
    const t0 = w("Korea's"), t1 = w("So");
    groups.push({ sun: "auto", id: "wrecks", place: "chilcheon", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet({ dusk: true }), light: DUSK, lens: { cInf: 6 },
      alive: [[t0, t1]],
      cam: [{ t: t0, pos: [-120, 9, 34], look: [-170, 1, 0], fov: 42, drift: 0.3 }, { t: t1, pos: [-128, 7.5, 26], look: [-172, 1.5, -2], fov: 40, glide: 1 }],
      people: [],
      rigs: [wreckRig([[-160, -8, 0.5], [-150, 10, -0.4], [-178, 4, 0.9], [-168, -22, -0.2], [-186, 20, 0.3]]),
        fleetRig((b) => japanese(b.k), [0, 1, 2, 3].map((k) => ({ x: -205 + k * 4, z: -40 + k * 16, yaw: -0.1, k })), (t) => ({ dx: -1.2 * (t - t0) })),
        burst([{ at: [-160, 3, -8], t: w("wiped"), size: 3 }, { at: [-150, 3, 10], t: w("fleet."), size: 2.4 }])] });
  }
  // ================= 5 the king tells Yi to come ashore (the throne hall at night, lamps)
  const KING: V3 = [0, 0.75, -4.0];
  {
    const t0 = w("So"), t1 = w("Yi", w("land.") - 0.1);
    groups.push({ sun: "auto", id: "court", place: "court", t0, t1, xfade: 0.6, set: () => courtSet(), light: "night", lens: { cInf: 8 },
      cam: [pair(t0, [KING, [1.1, 0, -1.6]], -4, 6, 40, 0.5)],
      people: [{ id: "king", at: () => KING, faceTo: () => [0, 0.75, 6], props: () => ({ costume: "jking", seed: 51, face: faceTrack(words, "furious", [{ word: "land.", face: "deadpan" }], t0), pose: poseTrack(words, "point", [["ashore", "sweep"], ["land.", "point"]], t0), quote: [[w("tells"), w("land.") + 0.3]] }) },
        { id: "off", at: () => [1.1, 0, -1.6], faceTo: () => KING, props: () => ({ costume: "official", seed: 52, face: "worried", kneel: 1, pose: "reach", item: "letter" }) }],
      rigs: [] });
  }
  // ================= 6 Yi writes back, "I still have ships." (night on his deck, a lamp, his twelve behind him)
  {
    const t0 = w("Yi", w("land.") - 0.1), t1 = w("Then");
    const desk = onDeck(FLAG, 6.2, 0.0, DECK_K);
    const Y: V3 = [desk[0] - 0.4, DECK_K, desk[2] + 1.0];
    groups.push({ sun: "auto", id: "letter", place: "yi-night", t0, t1, xfade: 0.6, set: () => straitSet({ night: true }), light: "night", lens: { cInf: 6 },
      cam: [{ ...cK(t0, [Y], "close", 60, 6, 40, 1, [[...desk.map((v, j) => v - (j === 1 ? 0 : 0.5)), desk[0] + 0.5, DECK_K + 0.9, desk[2] + 0.5] as Box]), drift: 0.5 },
        { ...cK(w("I"), [Y], "medium", 40, 10, 44), glide: 0.8 }],
      people: [{ id: "yi", at: () => Y, faceTo: () => [desk[0], DECK_K, desk[2]], props: (t) => yiProps(faceTrack(words, "focus", [{ word: '"I', face: "sly" }], t0), { pose: poseTrack(words, "hold", [['"I', "point"]], t0), item: "letter", quote: [[w('"I'), w("have") + 0.7]] }) }],
      rigs: [fleetRig((b) => korean(b.k === 0), KB), lanternGlows([[desk[0], DECK_K + 1.2, desk[2]], ...KB.slice(1).map((b): V3 => [b.x + 3, DECK_K + 2, b.z])], 3.2),
        (ctx) => { const tb = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.7, 0.8), new THREE.MeshLambertMaterial({ color: "#5a3a24" })); tb.position.set(desk[0], DECK_K + 0.35, desk[2]); tb.castShadow = true; ctx.root.add(tb); return () => {}; }] });
  }
  // ================= 7 he anchors them at the mouth of a narrow strait off Jindo island (high, labels)
  {
    const t0 = w("Then"), t1 = w("The", w("island.") - 0.1);
    const tAnch = w("anchors");
    const settle = (t: number, b: Berth) => ({ dx: -14 * (1 - sm((t - t0 + 0.4) / (tAnch - t0 + 0.6))) * (b.k === 0 ? 1 : 0.8) });
    groups.push({ sun: "auto", id: "anchor", place: "mouth", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet({ fog: 9 }), light: "day", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [-120, 120, -40], look: [40, 0, 0], fov: 44 }, { t: t1, pos: [-90, 96, -30], look: [44, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [fleetRig((b) => korean(b.k === 0), KB, settle), burst(KB.map((b) => ({ at: [b.x + 6, 0.5, b.z + 3.6] as V3, t: tAnch + (b.k % 4) * 0.12, size: 2.2 }))),
        label("JINDO ISLAND", [60, 26, -120], w("Jindo") - 0.1, t1 + 1, 7), label("KOREA", [60, 30, 140], w("narrow"), t1 + 1, 7), label("THE STRAIT", [70, 10, 0], w("strait"), t1 + 1, 6)] });
  }
  // ================= 8 the locals call it the crying strait: villagers on the Jindo rocks, hands over their ears, the
  // gap roaring below
  const V1: V3 = [72, landH(72, -53), -53], V2: V3 = [70.6, landH(70.6, -54), -54];
  {
    const t0 = w("The", w("island.") - 0.1), t1 = w("The", w("water.") - 0.1);
    groups.push({ sun: "auto", id: "locals", place: "jindo", t0, t1, xfade: 0.6, set: () => straitSet(), light: "day", lens: { cInf: 5 },
      alive: [[t0, t1]],
      cam: [{ ...cK(t0, [V1, V2], "medium", 200, 14, 42), drift: 0.6 }, { ...cK(t1, [V1, V2], "medium", 170, 20, 44), glide: 1.2 }],
      people: [{ id: "v1", at: () => V1, faceTo: () => [72, 0, 0], props: () => ({ costume: "villager", seed: 61, face: faceTrack(words, "grimace", [{ word: "roar", face: "scream" }], t0), pose: poseTrack(words, "point", [["crying", "cheeks"]], t0) }) },
        { id: "v2", at: () => V2, faceTo: () => [70, 0, 0], props: () => ({ costume: "villager2", seed: 62, face: faceTrack(words, "worried", [{ word: "roar", face: "squeeze" }], t0), pose: "cheeks" }) }],
      rigs: [currentRig((t) => -3.4 * t, () => 1), burst([0, 1, 2, 3, 4].map((k) => ({ at: [60 + k * 9, 0.4, -36 + (k % 2) * 30] as V3, t: t0 + 0.3 + k * 0.55, size: 3 }))),] });
  }
  // ================= 9 the Japanese fleet pours in with the current behind it (high, the streaks running west)
  const pour = (t0: number) => (t: number, b: Berth) => ({ dx: -4.2 * (t - t0) });
  {
    const t0 = w("The", w("water.") - 0.1), t1 = w("Ship");
    groups.push({ sun: "auto", id: "pour", place: "gap", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet({ fog: 8 }), light: "day", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [175, 70, 70], look: [60, 0, -6], fov: 46 }, { t: t1, pos: [150, 58, 64], look: [40, 0, -4], fov: 46, glide: 1 }],
      people: [],
      rigs: [currentRig((t) => -6 * t, () => 1), fleetRig((b) => japanese(b.k), JB.map((b) => ({ ...b, x: b.x + 40 })), pour(t0)), fleetRig((b) => korean(b.k === 0), KB)] });
  }
  // ================= 10 ship after ship after ship: low on the water as they sweep past, crews shouting
  {
    const t0 = w("Ship"), t1 = w("His", w("Ship"));
    const lane: Berth[] = [0, 1, 2].map((k) => ({ x: 84 + k * 22, z: 20, yaw: Math.PI, k: 40 + k }));
    const v = 13;
    const mv = (t: number) => -v * (t - t0);
    groups.push({ sun: "auto", id: "column", place: "gap-low", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet(), light: "day", lens: { cInf: 5 },
      cam: [{ t: t0, pos: [62, 6, 38], look: [86, 4, 18], fov: 44 }, { t: t1, pos: [60, 6, 37], look: [76, 4, 18], fov: 44, glide: 0.6 }],
      people: [],
      rigs: [currentRig((t) => -6 * t, () => 1), fleetRig((b) => japanese(b.k), lane, (t) => ({ dx: mv(t) })), fleetRig((b) => japanese(b.k), JB.filter((b) => b.x > 120).map((b) => ({ ...b, z: b.z - 10 })), pour(t0))] });
  }
  // ================= 11 his captains hang back and politely let the admiral go first (the flagship pulls ahead)
  const ahead = (t0: number) => (t: number, b: Berth) => ({ dx: b.k === 0 ? 22 * sm((t - t0) / 3.4) : 0 });
  {
    const t0 = w("His", w("Ship")), t1 = w("His", w("first.") - 0.1);
    const B = KB[2];
    const C1 = onDeck(B, 4.6, 0.9, DECK_K), C2 = onDeck(B, 3.4, -0.4, DECK_K);
    const back = (p: V3) => (_t: number): V3 => p;
    groups.push({ sun: "auto", id: "hangback", place: "kdeck", t0, t1, xfade: 0.6, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [{ ...pair(t0, [C1, C2], 196, 14, 46, 0) }], alive: [[t0, t1]],
      people: [
        { id: "c1", at: back(C1), faceTo: () => [YI[0] + 20, DECK_K, YI[2]], props: () => ({ costume: "jcaptain", seed: 41, face: faceTrack(words, "grin", [{ word: "politely", face: "sly" }], t0), pose: poseTrack(words, "stand", [["politely", "sweep"]], t0), marks: [markAt(words, "hang", "sweat")] }) },
        { id: "c2", at: back(C2), faceTo: () => [YI[0] + 20, DECK_K, YI[2]], props: () => ({ costume: "jcaptain2", seed: 42, face: faceTrack(words, "worried", [{ word: "admiral", after: t0, face: "grin" }], t0), pose: poseTrack(words, "stand", [["let", "sweep"]], t0) }) }],
      rigs: [westCur, fleetRig((b) => korean(b.k === 0), KB, ahead(t0)), fleetRig((b) => japanese(b.k), JB, japMove())] });
  }
  // ================= 12 his flagship fights almost alone: guns firing, the Japanese closing
  const FLAG2: Berth = { ...FLAG, x: FLAG.x + 60 };
  {
    const t0 = w("His", w("first.") - 0.1), t1 = w("Then", w("alone."));
    const Y = yiAt(FLAG2);
    const shots = [w("flagship"), w("fights"), w("almost"), w("alone.")];
    groups.push({ sun: "auto", id: "alone", place: "front", t0, t1, xfade: 0.6, set: () => straitSet(), light: lightArc([[t0, "golden"]], shots.map((t) => ({ kind: "flash" as const, t, frames: 2 }))), lens: { cInf: 5 },
      alive: [[t0, t1]],
      cam: [{ ...cK(t0, [Y], "close", -150, 10, 46), drift: 0 }, { ...cK(t1, [Y], "medium", -128, 16, 50), glide: 1 }],
      people: [{ id: "yi", at: () => Y, faceTo: () => [Y[0] + 10, Y[1], Y[2]], props: () => yiProps(faceTrack(words, "furious", [], t0), { pose: poseTrack(words, "point", [["fights", "armsUp"], ["almost", "point"]], t0) }) }],
      rigs: [currentRig(flowIn, () => 1), fleetRig((b) => korean(b.k === 0), [FLAG2]),
        fleetRig((b) => japanese(b.k), JB.slice(0, 14).map((b) => ({ ...b, x: b.x + 16 }))),
        burst(shots.map((t, i) => ({ at: [FLAG2.x + 2 + i * 1.5, 2.5, FLAG2.z + (i % 2 ? 4 : -4)] as V3, t, size: 3.2 }))),
        burst(shots.map((t, i) => ({ at: [JB[i].x + 16 - 6, 3, JB[i].z] as V3, t: t + 0.18, size: 3.6 }))),
        debris(shots.map((t, i) => ({ at: [JB[i].x + 16 - 6, 3, JB[i].z] as V3, t: t + 0.18, n: 22, kind: "splinter" as const, size: 0.3, floorY: 0.1, up: 4 }))),
        (ctx) => { const r = new Rising(14, "smoke", 5, 90); r.group.position.set(FLAG2.x + 4, 2, FLAG2.z); ctx.root.add(r.group); return (t) => r.update(t, clamp01((t - shots[0]) / 0.3), 10, 2.4, 8); }] });
  }
  // ================= 13 then, historians think, the roaring stops: Yi at the rail, the white water dying away
  {
    const t0 = w("Then", w("alone.")), t1 = w("You");
    const Y = yiAt(FLAG2, -1.5);
    const amp = (t: number) => 1 - sm((t - w("roaring")) / (tStops - w("roaring") + 0.4));
    let ph0 = 0; const slow = (t: number) => { const u = clamp01((t - t0) / (t1 - t0)); return -2.2 * (t0 + (t1 - t0) * (u - u * u * u / 3)); };
    void ph0;
    groups.push({ sun: "auto", id: "slack", place: "front", t0, t1, xfade: 0.6, set: () => straitSet(), light: lightArc([[t0, "golden"], [tStops, DUSKL, 0.8]]), lens: { cInf: 6 },
      alive: [[t0, t1]],
      cam: [{ ...cK(t0, [Y], "close", -70, 22, 40), drift: 0 }, { ...cK(t1, [Y], "medium", -60, 26, 44), glide: 1 }],
      people: [{ id: "yi", at: () => Y, faceTo: () => [Y[0], Y[1], Y[2] + 10], props: () => yiProps(faceTrack(words, "focus", [{ word: "stops.", face: "puzzled", react: [{ face: "blank", frames: 2 }] }], t0), { pose: poseTrack(words, "hold", [["roaring", "handIn"]], t0) }) }],
      rigs: [currentRig(slow, amp), fleetRig((b) => korean(b.k === 0), [FLAG2]), fleetRig((b) => japanese(b.k), JB.slice(0, 10).map((b) => ({ ...b, x: b.x + 18 })))] });
  }
  // ================= 14 you see, the water runs like a river and turns around four times a day (explain light, high)
  {
    const t0 = w("You"), t1 = w("The", w("day.") - 0.1);
    const tTurns = w("turns"), tFour = w("four");
    const ph = (t: number) => (t < tTurns ? -9 * (t - t0) : -9 * (tTurns - t0) + 9 * (t - tTurns));
    groups.push({ sun: "auto", id: "river", place: "explain", insert: true, t0, t1, xfade: 0.6, set: () => straitSet({ explain: true, fog: 14 }), light: "explain", lens: { cInf: 2 },
      cam: [{ t: t0, pos: [70, 190, -80], look: [70, 0, 0], fov: 44 }, { t: tTurns, pos: [150, 150, -110], look: [72, 0, 0], fov: 44, glide: 1 }, { t: t1, pos: [160, 135, -96], look: [74, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [currentRig(ph, (t) => 1 - 0.85 * Math.max(0, 1 - Math.abs(t - tTurns) / 0.35)), arrowsRig((t) => (t < tTurns ? -1 : 1), tTurns),
        tilted(1.1, counter({ at: [0, 0, 0], rotY: Math.PI, w: 30, digits: 1, from: 0, to: 4, t0, t1, steps: [[t0, 0], [tTurns, 1], [tFour, 2], [w("times") + 0.15, 3], [w("day."), 4]], label: "TURNS", unit: "A DAY" }), [76, 12, 22])] });
  }
  // ================= 15 they had ridden the current into a gap so narrow only a few could reach him (golden, high oblique)
  const jam = JB.map((b) => ({ ...b, x: b.x + 14 }));
  {
    const t0 = w("The", w("day.") - 0.1), t1 = w("And", w("reach"));
    const front = jam.slice(0, 3);
    groups.push({ sun: "auto", id: "gap", place: "gap", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [10, 80, -80], look: [100, 0, 0], fov: 44 }, { t: w("only"), pos: [40, 50, -50], look: [92, 0, 0], fov: 42, glide: 1 }, { t: t1, pos: [48, 44, -42], look: [92, 0, 2], fov: 42, glide: 1 }],
      people: [],
      rigs: [currentRig(flowIn, () => 1), fleetRig((b) => korean(b.k === 0), [FLAG2, ...KB.slice(1).map((b) => ({ ...b, x: b.x - 6 }))]), fleetRig((b) => japanese(b.k), jam),
        glints(front.map((b, i) => ({ at: [b.x, 12, b.z] as V3, t: w("few") + i * 0.12, size: 2.4 }))), label("ONLY A FEW CAN REACH HIM", [86, 20, 0], w("only"), t1 + 1, 4.6)] });
  }
  // ================= 16 and when it turned, that same current shoved their ships backwards into each other
  const tShoved = w("shoved");
  const drift = (t: number, b: Berth) => { const u = Math.max(0, t - tTurned); const k = 1 + ((b.k * 37) % 10) / 12; return { dx: 3.2 * u * u * k * 0.5 + 2.2 * u * k, dyaw: ((b.k * 53) % 7 - 3) * 0.08 * Math.min(1, u), heel: ((b.k * 17) % 5 - 2) * 0.03 * Math.min(1, u) }; };
  {
    const t0 = w("And", w("reach")), t1 = tShoved;
    groups.push({ sun: "auto", id: "turn", place: "gap", establishing: true, t0, t1, xfade: 0.6, set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [20, 48, 60], look: [80, 0, 0], fov: 44 }, { t: t1, pos: [30, 44, 54], look: [88, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [currentRig((t) => (t < tTurned ? -2.2 * t : -2.2 * tTurned + 5 * (t - tTurned)), (t) => (t < tTurned ? 0.3 : Math.min(1, 0.3 + (t - tTurned) * 2))), arrowsRig((t) => (t < tTurned ? -1 : 1), tTurned, 0.6),
        fleetRig((b) => korean(b.k === 0), [FLAG2, ...KB.slice(1).map((b) => ({ ...b, x: b.x - 6 }))]), fleetRig((b) => japanese(b.k), jam, drift)] });
  }
  {
    const t0 = tShoved, t1 = w("Korean");
    const A: Berth = { x: 70, z: 6, yaw: Math.PI - 0.15, k: 60 }, B2: Berth = { x: 81, z: 3, yaw: Math.PI + 0.25, k: 61 };
    const tHit = w("into", tShoved) - 0.05;
    const mA = (t: number) => ({ dx: 4 * sm((t - t0) / (tHit - t0)), dyaw: 0.5 * sm((t - tHit) / 0.6), heel: t > tHit ? 0.12 * Math.sin((t - tHit) * 6) * Math.exp(-(t - tHit)) : 0 });
    const mB = (t: number) => ({ dx: 1.5 * sm((t - t0) / (tHit - t0)), dyaw: -0.4 * sm((t - tHit) / 0.6), heel: t > tHit ? -0.12 * Math.sin((t - tHit) * 6) * Math.exp(-(t - tHit)) : 0 });
    const crewA = [[2.4, 0.9], [0.2, -1.0]].map(([lx, lz], j): PersonSpec => ({ id: `ca${j}`, at: (t) => { const m = mA(t); return onDeck({ ...A, x: A.x + m.dx, yaw: A.yaw + m.dyaw }, lx, lz, DECK_J); }, faceTo: () => [B2.x, DECK_J, B2.z],
      props: () => ({ costume: j ? "ashigaru" : "samurai", seed: 81 + j, face: faceTrack(words, "worried", [{ word: "into", after: tShoved, face: "terrified", react: [{ face: "scream", frames: 3 }] }], t0), pose: [{ t: t0, v: "point" }, { t: tHit, v: "armsUp" }] }) }));
    groups.push({ sun: "auto", id: "crash", place: "gap-low", t0, t1, xfade: 0.6, set: () => straitSet(), light: "golden", lens: { cInf: 5 },
      alive: [[t0, t1]],
      cam: [pair(t0, [...crewA.map((p) => p.at(t0)), ...crewA.map((p) => p.at(t1)), ...crewA.map((p) => p.at(tHit + 0.3))], 28, 12, 52, 0.4)],
      people: crewA,
      rigs: [currentRig((t) => 5 * t, () => 1), fleetRig((b) => japanese(b.k), [A], (t) => mA(t)), fleetRig((b) => japanese(b.k), [B2], (t) => mB(t)),
        burst([{ at: [78, 3, 4], t: tHit, size: 4 }, { at: [79, 4, 5], t: tHit + 0.25, size: 3 }]),
        debris([{ at: [78, 3.5, 4], t: tHit, n: 40, kind: "splinter", size: 0.35, floorY: 0.1, up: 5, speed: 4 }])] });
  }
  // ================= 17 Korean records count thirty-one Japanese ships lost, and none of his (dusk: a scribe on Yi's
  // deck, the tally board; wrecks burning in the strait; then the second board, 0)
  {
    const t0 = w("Korean"), t1 = w("The", w("none"));
    const tNone = w("none");
    const S: V3 = onDeck(FLAG, 5.0, 1.0, DECK_K);
    const board: V3 = ((p: V3): V3 => [p[0], DECK_K + 1.75, p[2]])(onDeck(FLAG, 6.3, -1.3, DECK_K));
    const bb: Box = [board[0] - 0.7, board[1] - 1.1, board[2] - 0.2, board[0] + 0.7, board[1] + 0.4, board[2] + 0.2];
    const k0 = fit(t0, [personBox(S), bb], 50, 10, 44, { b: 0.3, t: 0.12, x: 0.1 });
    const face = Math.atan2(k0.pos[0] - board[0], k0.pos[2] - board[2]);
    groups.push({ sun: "auto", id: "records", place: "yi-dusk", t0, t1, xfade: 0.6, set: () => straitSet({ dusk: true }), light: DUSK, lens: { cInf: 6 },
      alive: [[t0, t1]],
      cam: [{ ...k0, drift: 0 },
        { ...fit(tNone - 0.1, [personBox(S), bb], 82, 18, 44, { b: 0.3, t: 0.12, x: 0.1 }), glide: 0.8 }],
      people: [{ id: "scribe", at: () => S, faceTo: () => board, props: () => ({ costume: "official", seed: 91, face: faceTrack(words, "focus", [{ word: "thirty-one", face: "grin" }, { word: "none", face: "smug" }], t0), pose: poseTrack(words, "hold", [["count", "point"], ["none", "hips"]], t0), item: "letter" }) }],
      rigs: [fleetRig((b) => korean(b.k === 0), KB), wreckRig([[80, -14, 0.4], [96, 16, -0.5], [112, -4, 0.8], [128, 20, 0.2], [104, -26, -0.3]]),
        counter({ at: board, rotY: face, w: 1.15, digits: 2, from: 0, to: 31, t0, t1, steps: [[t0, 0], [w("thirty-one") + 0.2, 31]], label: "JAPAN", unit: "SHIPS LOST" }),
        shownFrom(tNone - 0.05, counter({ at: [board[0], board[1] - 0.72, board[2]], rotY: face, w: 1.15, digits: 2, from: 0, to: 0, t0: tNone, t1, steps: [[t0, 0]], label: "YI", unit: "SHIPS LOST" })),
        lanternGlows([[S[0] - 0.8, DECK_K + 1.6, S[2] + 1.0]], 2.6)] });
  }
  // ================= 18 the king thought Yi had no navy left (the hall, the king scoffs)
  {
    const t0 = w("The", w("none")), t1 = w("but");
    groups.push({ sun: "auto", id: "king2", place: "court", t0, t1, xfade: 0.6, set: () => courtSet(), light: "night", lens: { cInf: 8 },
      cam: [{ ...cK(t0, [KING], "close", -14, 4, 36), drift: 0 }, { ...cK(t1, [KING], "close", 8, 6, 34), glide: 1 }],
      people: [{ id: "king", at: () => KING, faceTo: () => [0, 0.75, 6], props: () => ({ costume: "jking", seed: 51, face: faceTrack(words, "smug", [{ word: "left,", face: "cackle" }], t0), pose: poseTrack(words, "hips", [["no", "shrug"]], t0) }) }],
      rigs: [] });
  }
  // ================= 19 but he had a sea that changes sides: Yi at his bow at dusk, the current running east now, lamps
  // lit along his thirteen, the camera rising away to the end
  {
    const t0 = w("but"), t1 = END;
    const Y = yiAt(FLAG2);
    groups.push({ sun: "auto", id: "last", place: "yi-dusk", t0, t1, xfade: 0.6, set: () => straitSet({ dusk: true }), light: DUSK, lens: { cInf: 5 },
      alive: [[t0, t1]],
      cam: [{ ...cK(t0, [Y], "close", -110, 6, 40), drift: 0 }, { ...cK(w("sea"), [Y], "medium", -125, 14, 44), glide: 1 }, { ...cK(t1, [Y], "wide", -140, 24, 48), glide: 1 }],
      people: [{ id: "yi", at: () => Y, faceTo: () => [Y[0] + 10, Y[1], Y[2]], props: () => yiProps(faceTrack(words, "focus", [{ word: "sea", face: "sly" }], t0), { pose: poseTrack(words, "hips", [["changes", "point"]], t0) }) }],
      rigs: [currentRig(flowOut, () => 1), fleetRig((b) => korean(b.k === 0), [FLAG2, ...KB.slice(1)]), lanternGlows([[Y[0] - 1.5, DECK_K + 1.8, Y[2] + 1.5], ...KB.slice(1).map((b): V3 => [b.x + 3, DECK_K + 2, b.z])], 3.4),
        wreckRig([[140, -16, 0.4], [156, 18, -0.5], [176, -2, 0.8]])] });
  }
  void PRESETS; void Flame; void DECK_J;
  return { groups };
}

/** the low desk for the hook: the king's order (a yellow scroll with a red seal) and Yi's reply with its first lines */
function orderDesk(D: V3): Rig {
  return (ctx) => {
    const g = new THREE.Group(); g.position.set(...D); ctx.root.add(g);
    const wood = new THREE.MeshLambertMaterial({ color: "#5a3a24" });
    const top = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.08, 0.7), wood); top.position.y = 0.42; top.castShadow = true; g.add(top);
    for (const [x, z] of [[-0.48, -0.28], [0.48, -0.28], [-0.48, 0.28], [0.48, 0.28]]) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.4, 0.07), wood); l.position.set(x, 0.2, z); g.add(l); }
    const paper = (w: number, h: number, draw: (c: CanvasRenderingContext2D) => void) => { const c = document.createElement("canvas"); c.width = 256; c.height = Math.round(256 * h / w); const x = c.getContext("2d")!; draw(x);
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshLambertMaterial({ map: t })); m.rotation.x = -Math.PI / 2; return m; };
    const order = paper(0.5, 0.34, (x) => { x.fillStyle = "#e9c96a"; x.fillRect(0, 0, 256, 174); x.fillStyle = "#3a2a1c"; for (let k = 0; k < 7; k++) x.fillRect(24 + k * 30, 20, 8, 110); x.fillStyle = "#c0392b"; x.fillRect(170, 112, 52, 52); });
    order.position.set(-0.25, 0.47, -0.08); order.rotation.z = 0.15; g.add(order);
    const reply = paper(0.42, 0.3, (x) => { x.fillStyle = "#f4ecd8"; x.fillRect(0, 0, 256, 183); x.fillStyle = "#1e1b26"; for (let k = 0; k < 3; k++) x.fillRect(180 - k * 34, 20, 9, 120); });
    reply.position.set(0.28, 0.47, 0.08); reply.rotation.z = -0.1; g.add(reply);
    return () => {};
  };
}
/** a rig whose objects appear only from t0 */
function shownFrom(t0: number, r: Rig): Rig {
  return (ctx) => { const h = new THREE.Group(); ctx.root.add(h); const f = r({ ...ctx, root: h }); return (t, cam) => { h.visible = t >= t0; f(t, cam); }; };
}
/** a rig drawn inside a holder group at p tilted by rx (radians about x) */
function tilted(rx: number, r: Rig, p: V3): Rig {
  return (ctx) => { const h = new THREE.Group(); h.position.set(...p); h.rotation.x = rx; ctx.root.add(h); return r({ ...ctx, root: h }); };
}
/** big glowing chevrons on the water showing the current's direction (dir -1 west, +1 east); they swing round at tFlip */
function arrowsRig(dir: (t: number) => number, tFlip: number, scale = 1): Rig {
  return (ctx) => {
    const shape = new THREE.Shape(); shape.moveTo(0, 0); shape.lineTo(-6, 4); shape.lineTo(-4, 0); shape.lineTo(-6, -4); shape.lineTo(0, 0);
    const geo = new THREE.ShapeGeometry(shape); geo.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({ color: "#ffe08a", transparent: true, opacity: 0.95, depthWrite: false, fog: false });
    const ar = [-30, 10, 50, 90, 130, 170].flatMap((x, i) => [-18, 0, 18].map((z, j) => { const m = new THREE.Mesh(geo, mat); m.position.set(x + (j % 2) * 10, 0.3, z * (x > 30 && x < 110 ? 0.9 : 1.6)); m.scale.setScalar(2.2 * scale); m.layers.set(3); m.renderOrder = 5; ctx.root.add(m); return { m, x0: m.position.x, i: i * 3 + j }; }));
    return (t) => {
      const d = dir(t), u = clamp01((t - tFlip) / 0.35);
      const rot = d < 0 && t < tFlip ? Math.PI : Math.PI * (1 - sm(u));
      for (const a of ar) { const travel = ((t * 9 * (t < tFlip ? -1 : 1)) % 40 + 40) % 40; a.m.position.x = a.x0 + travel - 20; a.m.rotation.y = rot; }
    };
  };
}
