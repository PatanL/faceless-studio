// story-myeongnyang v3 (our own code): the anonymous Storm Oil form. An admiral anchors his last ships in a roaring
// channel, drops a cork and waits; the enemy rides the current in, only a few fit, the cork stops, the tide turns and
// shoves them back into each other. The reversing tide is the only stated fact; everything else is invented.
// The opening shot is the hook lab's MyeongHook (src/study/myeong/hook.tsx), reused as group 1. Groups are anchored
// on the Kokoro (am_eric) word timings; the joins follow the RicksClips mix (dissolves 5-8 f, a few whips, one cut,
// one match dissolve), and the gates stay failing.
import * as THREE from "three";
import type { GroupSpec, PersonSpec, V3, Rig } from "../kit/Stage";
import type { Timing } from "../kit/timing";
import { fit, tagSprite, sm, personBox } from "../kit/framing";
import { castKey } from "../kit/castframe";
import type { CamKey } from "../kit/campath";
import { faceTrack, poseTrack, wordT, markAt, type Word } from "../kit/acting";
import { burst, debris, glints } from "../kit/fx2";
import { lightArc, mixKey } from "../kit/lightarc";
import { Rising } from "../kit/fx";
import { NOINK } from "../ink";
import { straitSet, currentRig, fleetRig, korean, japanese, japaneseFleet, onDeck, wreckRig, DECK_K, DECK_J, type Berth } from "./sets";
import { arrowsRig } from "./story";
import { buildHook } from "../study/myeong/hook";

export type MyeongStory = { groups: GroupSpec[] };

const clamp01 = (u: number) => Math.min(1, Math.max(0, u));
const cK = (t: number, feet: V3[], preset: "close" | "medium" | "wide", az: number, el: number, fov: number, s = 1): CamKey =>
  ({ ...castKey(t, feet, preset, az, el, fov, s), drift: preset === "wide" ? 0.3 : preset === "close" ? 0.5 : 0.4 });
const pair = (t: number, ps: V3[], az: number, el: number, fov = 40, drift = 0.3): CamKey => ({ ...fit(t, ps.map((p) => personBox(p)), az, el, fov, { b: 0.34, t: 0.16, x: 0.14 }), drift });
const D = (frames = 6) => ({ kind: "dissolve" as const, frames });
const WHIP = { kind: "whip" as const };
/** a world label that pops in at t0 and out at t1 */
const label = (text: string, at: V3, t0: number, t1: number, h = 1.2): Rig => (ctx) => {
  const s = tagSprite(text, h); ctx.root.add(s);
  const mat = (s as THREE.Sprite).material as THREE.SpriteMaterial;
  return (t) => { s.position.set(...at); const o = sm((t - t0) / 0.12) * (1 - sm((t - t1) / 0.12)); s.visible = o > 0.01; mat.opacity = o; };
};
/** the cork: a fat cartoon wine cork lying on the water at pos(t), bobbing, with a fading ripple ring; before tLand
 * it falls from the admiral's hand (from) to the water */
const corkRig = (pos: (t: number) => V3, from?: V3, tDrop = 0, tLand = 0): Rig => (ctx) => {
  const g = new THREE.Group(); ctx.root.add(g);
  const body = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.23, 0.42, 18), new THREE.MeshLambertMaterial({ color: "#d4a462" }));
  body.rotation.z = Math.PI / 2; body.castShadow = true; g.add(body);
  for (const s of [-1, 1]) { const end = new THREE.Mesh(new THREE.CylinderGeometry(s < 0 ? 0.231 : 0.201, s < 0 ? 0.231 : 0.201, 0.02, 18), new THREE.MeshLambertMaterial({ color: "#8a5a2c" })); end.rotation.z = Math.PI / 2; end.position.x = s * 0.21; g.add(end); }
  const ring = new THREE.Mesh(new THREE.RingGeometry(0.34, 0.42, 36), new THREE.MeshBasicMaterial({ color: "#f4fbff", transparent: true, depthWrite: false }));
  ring.rotation.x = -Math.PI / 2; ring.layers.set(NOINK); ctx.root.add(ring);
  const splash = from ? burst([{ at: pos(tLand), t: tLand, size: 1.2, n: 10 }])(ctx) : null;
  return (t, cam) => {
    let p = pos(t);
    if (from && t < tLand) { const u = clamp01((t - tDrop) / (tLand - tDrop)); p = [from[0] + (p[0] - from[0]) * u, from[1] + (p[1] - from[1]) * u * u, from[2] + (p[2] - from[2]) * u]; }
    g.position.set(p[0], p[1] + (from && t < tLand ? 0 : 0.03 * Math.sin(t * 3.1)), p[2]);
    g.rotation.set(0.15 * Math.sin(t * 2.3), 0.4 + 0.2 * Math.sin(t * 0.7), 0.08 * Math.sin(t * 2.9));
    const ph = (t * 1.6) % 1; ring.visible = !from || t >= tLand; ring.position.set(p[0], 0.07, p[2]); ring.scale.setScalar(1 + ph * 1.6);
    (ring.material as THREE.MeshBasicMaterial).opacity = 0.8 * (1 - ph);
    splash?.(t, cam);
  };
};
/** an anchor rope from a deck point down into the water, taut against the current */
const ropeRig = (a: V3, b: V3): Rig => (ctx) => {
  const d = new THREE.Vector3(b[0] - a[0], b[1] - a[1], b[2] - a[2]), len = d.length();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, len, 8), new THREE.MeshLambertMaterial({ color: "#d8b070" }));
  m.position.set((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); ctx.root.add(m);
  return () => {};
};

export function buildStory(T: Timing): MyeongStory {
  const words = T.words as Word[];
  const w = (word: string, after = -1, n = 1) => wordT(words, word, n, after);
  const END = words[words.length - 1].end + 0.4;
  const groups: GroupSpec[] = [];
  const add = (g: GroupSpec) => groups.push({ sun: "auto", ...g } as GroupSpec);
  const DUSK = mixKey("golden", "fire", 0.45);

  // ---- the world: his flagship at the channel mouth (x 16, bow +x toward the enemy), his other ships well behind
  // him (-x); the enemy (+x) rides the current in (-x) until the tide turns
  const FLAG: Berth = { x: 16, z: 0, yaw: 0, k: 0 };
  const BEHIND: Berth[] = Array.from({ length: 12 }, (_, i) => { const k = i + 1, p = Math.ceil(k / 2); return { x: 16 - 24 - 7.5 * p, z: (k % 2 ? 1 : -1) * (11 + 0.5 * p), yaw: 0, k }; });
  const MINE = [FLAG, ...BEHIND];
  const JB: Berth[] = japaneseFleet(84);
  const ADM = onDeck(FLAG, 6.0, 2.4, DECK_K), CAP = onDeck(FLAG, 4.9, 1.2, DECK_K);
  const HAND: V3 = [ADM[0] + 0.3, DECK_K + 1.0, ADM[2] + 0.9];
  const admProps = (face: unknown, pose: unknown, extra: Record<string, unknown> = {}) => ({ costume: "yi", seed: 13, face, pose, ...extra });
  const capProps = (face: unknown, pose: unknown, extra: Record<string, unknown> = {}) => ({ costume: "jcaptain", seed: 41, face, pose, ...extra });
  const westCur = currentRig((t) => -6 * t, () => 1);
  const myFleet = fleetRig((b) => korean(b.k === 0, true), MINE);
  const pour = (t0: number, v = 4.2) => (t: number) => ({ dx: -v * (t - t0) });

  // ================= 1 the hook (src/study/myeong/hook.tsx, MyeongHook): he lets the anchor go, the fleet beyond
  const tHear = w("could");
  {
    const h = buildHook().groups[0];
    add({ ...h, t0: 0, t1: tHear, alive: [[0, tHear]] });
  }
  // ================= 2 "...he could hear them laughing": the enemy crews cackling at him from their decks
  {
    const t0 = tHear, t1 = w("His", 5);
    const LEAD: Berth = { x: 70, z: 2, yaw: Math.PI, k: 1 };
    const mv = (t: number) => -2.4 * (t - t0);
    const S1 = (t: number) => onDeck({ ...LEAD, x: LEAD.x + mv(t) }, 3.4, 0.5, DECK_J), S2 = (t: number) => onDeck({ ...LEAD, x: LEAD.x + mv(t) }, 2.2, -0.7, DECK_J);
    add({ id: "laugh", place: "jdeck", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 5 },
      cam: [pair(t0, [S1(t0), S2(t0)], -70, 10, 44, 0), { ...pair(t1, [S1(t1), S2(t1)], -58, 12, 42, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "s1", at: S1, faceTo: () => ADM, props: () => ({ costume: "samurai", seed: 31, face: faceTrack(words, "grin", [{ word: "laughing.", face: "cackle", react: [{ face: "squeeze", frames: 2 }] }], t0), pose: poseTrack(words, "point", [["laughing.", "laugh"]], t0) }) },
        { id: "s2", at: S2, faceTo: () => ADM, props: () => ({ costume: "ashigaru", seed: 32, face: faceTrack(words, "smug", [{ word: "laughing.", face: "cackle" }], t0 + 0.1), pose: [{ t: t0, v: "laugh" }, { t: w("laughing.") + 0.13, v: "armsUp" }] }) }],
      rigs: [westCur, fleetRig((b) => japanese(b.k), [LEAD], (t) => ({ dx: mv(t) })), fleetRig((b) => japanese(b.k), JB.slice(0, 20), pour(0, 2.4))] });
  }
  // ================= 3 his captain grabs his collar (on his deck; he stays still)
  {
    const t0 = w("His", 5), t1 = w('"They\'ve');
    const C = onDeck(FLAG, 5.5, 1.85, DECK_K);   // at arm's length: his straight arm ends at the collar
    add({ id: "collar", place: "mydeck", t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [pair(t0, [ADM, C], -30, 8, 40, 0), { ...pair(t1, [ADM, C], -22, 8, 36, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => [ADM[0] + 10, ADM[1], ADM[2]], props: () => admProps(faceTrack(words, "focus", [{ word: "collar.", face: "deadpan" }], t0), "stand") },
        { id: "cap", at: () => C, faceTo: () => ADM, props: () => capProps(faceTrack(words, "angry", [{ word: "grabs", face: "angry" }], t0), "point", { marks: [markAt(words, "collar.", "sweat")] }) }],
      rigs: [westCur, myFleet, fleetRig((b) => japanese(b.k), JB, pour(0, 0.9))] });
  }
  // ================= 4 "They've brought ten ships for every one we have": high, his one flagship against the many
  {
    const t0 = w('"They\'ve'), t1 = w("and", w("have,"));
    add({ id: "odds", place: "mouth", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [-8, 26, -26], look: [40, 0, 0], fov: 46, drift: 0.3 }, { t: t1, pos: [-4, 24, -24], look: [44, 0, 0], fov: 46, glide: 1 }],
      people: [],
      rigs: [westCur, myFleet, fleetRig((b) => japanese(b.k), JB, pour(t0, 1.2)),
        label("10", [120, 18, 0], w("ten") - 0.05, t1 + 1, 12), label("1", [16, 10, 0], w("one", w("every")) - 0.05, t1 + 1, 5)] });
  }
  // ================= 5 "...and you're parking?": the captain close, screaming
  {
    const t0 = w("and", w("have,")), t1 = w("He", t0);
    add({ id: "parking", place: "mydeck", t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet(), light: "golden", lens: { cInf: 7 },
      cam: [cK(t0, [CAP], "close", -20, 6, 38), { ...cK(t1, [CAP], "close", -14, 4, 34), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "cap", at: () => CAP, faceTo: () => ADM, props: () => capProps(faceTrack(words, "angry", [{ word: 'parking?"', face: "scream", react: [{ face: "squeeze", frames: 2 }] }], t0), poseTrack(words, "shrug", [['parking?"', "armsUp"]], t0), { marks: [markAt(words, 'parking?"', "sweat")] }) }],
      rigs: [westCur, myFleet] });
  }
  // ================= 6 he doesn't look up (close on him; the captain still ranting behind)
  const tDrops = w("drops");
  {
    const t0 = w("He", w("and", w("have,"))), t1 = tDrops - 0.2;
    add({ id: "nolook", place: "mydeck", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [cK(t0, [ADM], "close", -48, 6, 38), { ...cK(t1, [ADM], "close", -40, 4, 34), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => [ADM[0], ADM[1], ADM[2] + 10], props: () => admProps(faceTrack(words, "deadpan", [{ word: "doesn't", face: "blank" }], t0), "hold") },
        { id: "cap", at: () => CAP, faceTo: () => ADM, props: () => capProps(faceTrack(words, "scream", [{ word: "look", face: "angry" }], t0 + 0.1), "armsUp") }],
      rigs: [westCur, myFleet] });
  }
  // ================= 7 he drops a cork over the side and watches it drift (an insert at the water by his hull)
  const CORK0: V3 = [ADM[0] + 0.3, 0.08, 4.5];
  const tLand = w("cork") + 0.2;
  const corkIn = (t: number): V3 => [CORK0[0] - 0.75 * Math.max(0, t - tLand), 0.08, CORK0[2]];
  {
    const t0 = tDrops - 0.2, t1 = w('"Wait');
    const camAt = (t: number, k: CamKey["t"]): CamKey => { const c = corkIn(t); return { t: k, pos: [c[0] + 1.6, 1.3, c[2] + 3.6], look: [c[0] - 0.2, t < tLand ? 0.9 : 0.2, c[2]], fov: 42 }; };
    add({ id: "corkdrop", place: "water", insert: true, t0, t1, xfade: 0.2, join: D(5), set: () => straitSet(), light: "golden", lens: { cInf: 9 },
      cam: [{ ...camAt(t0, t0), drift: 0 }, { ...camAt(tLand, tLand), glide: 0.5 }, { ...camAt(t1, t1), glide: 1 }],
      people: [],
      rigs: [currentRig((t) => -0.75 * t, () => 0.6), myFleet, corkRig(corkIn, [CORK0[0] + 0.1, 2.3, CORK0[2] - 0.2], t0 - 0.15, tLand)] });
  }
  // ================= 8 "Wait for the water... Watch the cork." (the pair on deck, he points down at the water)
  {
    const t0 = w('"Wait'), t1 = w("Then");
    add({ id: "wait", place: "mydeck", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [pair(t0, [ADM, CAP], 8, 8, 40, 0), { ...pair(w('"Watch'), [ADM, CAP], -4, 10, 38, 0), glide: 1 }, { ...pair(t1, [ADM, CAP], -8, 10, 36, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => CAP, props: () => admProps(faceTrack(words, "focus", [{ word: '"Watch', face: "sly" }], t0), poseTrack(words, "hold", [['"Watch', "point"]], t0)) },
        { id: "cap", at: () => CAP, faceTo: () => ADM, props: () => capProps(faceTrack(words, "worried", [{ word: 'cork."', face: "stunned", react: [{ face: "blank", frames: 2 }] }], t0 + 0.13), poseTrack(words, "shrug", [['cork."', "facepalm"]], t0)) }],
      rigs: [westCur, myFleet] });
  }
  // ================= 9 the enemy charges into the channel (high, the fleet pouring in)
  {
    const t0 = w("Then"), t1 = w("the", w("channel,", w("Then")));
    add({ id: "charge", place: "gap", establishing: true, t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet({ fog: 8 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [210, 62, 64], look: [80, 0, -4], fov: 46 }, { t: t1, pos: [190, 52, 58], look: [64, 0, -4], fov: 46, glide: 1 }],
      people: [],
      rigs: [currentRig((t) => -6 * t, () => 1), fleetRig((b) => japanese(b.k), JB.map((b) => ({ ...b, x: b.x + 30 })), pour(t0)), myFleet] });
  }
  // ================= 10 "...the current carrying them in like a river": low on the water as they sweep past
  {
    const t0 = w("the", w("channel,", w("Then"))), t1 = w("Their");
    const lane: Berth[] = [0, 1, 2].map((k) => ({ x: 84 + k * 22, z: 20, yaw: Math.PI, k: 40 + k }));
    add({ id: "river", place: "gap-low", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 5 },
      cam: [{ t: t0, pos: [62, 6, 38], look: [86, 4, 18], fov: 44 }, { t: t1, pos: [60, 6, 37], look: [76, 4, 18], fov: 44, glide: 0.6 }],
      people: [],
      rigs: [currentRig((t) => -9 * t, () => 1), fleetRig((b) => japanese(b.k), lane, (t) => ({ dx: -13 * (t - t0) })), fleetRig((b) => japanese(b.k), JB.filter((b) => b.x > 120).map((b) => ({ ...b, z: b.z - 10 })), pour(t0))] });
  }
  // ================= 11 their admiral is thrilled; the sea does the rowing (his rowers lounge, oars up)
  {
    const t0 = w("Their"), t1 = w("His", w("rowing."));
    const JF: Berth = { x: 74, z: -4, yaw: Math.PI, k: 2 };
    const at = (lx: number, lz: number) => (t: number) => onDeck({ ...JF, x: JF.x - 2 * (t - t0) }, lx, lz, DECK_J);
    const EA = at(6.2, 0.9), R1 = at(5.4, -1.0);
    add({ id: "thrilled", place: "jflag", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [cK(t0, [EA(t0), R1(t0)], "medium", -100, 8, 40), { ...cK(w("The", t0 + 1), [EA(w("The", t0 + 1)), R1(w("The", t0 + 1))], "medium", -84, 8, 38), glide: 1 }, { ...cK(t1, [EA(t1), R1(t1)], "medium", -80, 8, 36), glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "ea", at: EA, faceTo: () => [0, DECK_J, -4], props: () => ({ costume: "samurai2", seed: 71, face: faceTrack(words, "grin", [{ word: "thrilled.", face: "cackle" }], t0), pose: poseTrack(words, "point", [["thrilled.", "armsUp"]], t0) }) },
        { id: "rower", at: R1, faceTo: () => [100, DECK_J, -4], props: () => ({ costume: "ashigaru", seed: 72, face: faceTrack(words, "sleepy", [{ word: "rowing.", face: "bliss" }], t0), pose: "hips" }) }],
      rigs: [currentRig((t) => -6 * t, () => 1), fleetRig((b) => japanese(b.k), [JF], (t) => ({ dx: -2 * (t - t0) })), fleetRig((b) => japanese(b.k), JB.slice(4, 30), pour(t0, 2))] });
  }
  // ================= 12 his own captains anchor well behind him (high from astern: anchors splash along the rear line)
  {
    const t0 = w("His", w("rowing.")), t1 = w("politely");
    const tA = w("anchor");
    add({ id: "behind", place: "rear", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [-90, 48, -40], look: [10, 0, 0], fov: 44 }, { t: t1, pos: [-80, 42, -36], look: [14, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [westCur, fleetRig((b) => korean(b.k === 0, b.k !== 0), MINE, (t, b) => ({ dx: b.k ? 6 * (1 - sm((t - t0) / (tA - t0 + 0.4))) : 0 })),
        burst(BEHIND.map((b) => ({ at: [b.x + 7, 0.5, b.z + 3.4] as V3, t: tA + (b.k % 4) * 0.1, size: 2.4 }))),
        label("HIM", [16, 12, 0], w("well", t0) - 0.2, t1 + 1, 4)] });
  }
  // ================= 13 "...politely letting him face the enemy first": two captains bowing him on
  {
    const t0 = w("politely"), t1 = w("But");
    const B = BEHIND[1];
    const C1 = onDeck(B, 4.6, 0.9, DECK_K), C2 = onDeck(B, 3.4, -0.4, DECK_K);
    add({ id: "polite", place: "reardeck", t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [pair(t0, [C1, C2], 24, 12, 44, 0), { ...pair(t1, [C1, C2], 14, 12, 40, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "c1", at: () => C1, faceTo: () => [100, DECK_K, 0], props: () => ({ costume: "jcaptain2", seed: 42, face: faceTrack(words, "grin", [{ word: "politely", face: "sly" }], t0), pose: poseTrack(words, "stand", [["politely", "sweep"]], t0) }) },
        { id: "c2", at: () => C2, faceTo: () => [100, DECK_K, 0], props: () => ({ costume: "jsailor", seed: 43, face: faceTrack(words, "worried", [{ word: "face", face: "grin" }], t0 + 0.1), pose: poseTrack(words, "stand", [["face", "sweep"]], t0) }) }],
      rigs: [westCur, myFleet] });
  }
  // ================= 14 the channel is so narrow only a few ships fit at once (high oblique, label)
  const FRONT: Berth[] = JB.slice(0, 40).map((b) => ({ ...b, x: b.x - 40 }));
  {
    const t0 = w("But"), t1 = w("and", w("once,"));
    add({ id: "narrow", place: "gap", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [-20, 80, -80], look: [70, 0, 0], fov: 44 }, { t: w("only", t0), pos: [0, 50, -50], look: [62, 0, 0], fov: 42, glide: 1 }, { t: t1, pos: [8, 44, -42], look: [62, 0, 2], fov: 42, glide: 1 }],
      people: [],
      rigs: [westCur, myFleet, fleetRig((b) => japanese(b.k), FRONT),
        glints(FRONT.slice(0, 3).map((b, i) => ({ at: [b.x, 12, b.z] as V3, t: w("few") + i * 0.12, size: 2.4 }))), label("ONLY A FEW FIT", [56, 20, 0], w("only", t0), t1 + 1, 4.6)] });
  }
  // ================= 15 "...and his cannons keep those busy" (close on him, his guns firing)
  {
    const t0 = w("and", w("once,")), t1 = w("Meanwhile,");
    const shots = [w("cannons", t0), w("keep", t0), w("busy.")];
    add({ id: "cannons", place: "mydeck", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: lightArc([[t0, "golden"]], shots.map((t) => ({ kind: "flash" as const, t, frames: 2 }))), lens: { cInf: 5 },
      cam: [cK(t0, [ADM], "close", -70, 8, 44), { ...cK(t1, [ADM], "medium", -58, 12, 46), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => [ADM[0] + 10, ADM[1], ADM[2]], props: () => admProps(faceTrack(words, "focus", [{ word: "busy.", face: "smug" }], t0), poseTrack(words, "hold", [["cannons", "point"]], t0)) }],
      rigs: [westCur, myFleet, fleetRig((b) => japanese(b.k), FRONT),
        burst(shots.map((t, i) => ({ at: [FLAG.x + 9 + i * 0.5, 2.6, FLAG.z + (i % 2 ? 3 : -3)] as V3, t, size: 3.2 }))),
        burst(shots.map((t, i) => ({ at: [FRONT[i].x - 6, 3, FRONT[i].z] as V3, t: t + 0.18, size: 3.6 }))),
        debris(shots.map((t, i) => ({ at: [FRONT[i].x - 6, 3, FRONT[i].z] as V3, t: t + 0.18, n: 22, kind: "splinter" as const, size: 0.3, floorY: 0.1, up: 4 }))),
        (ctx) => { const r = new Rising(14, "smoke", 5, 90); r.group.position.set(FLAG.x + 10, 2, FLAG.z); ctx.root.add(r.group); return (t) => r.update(t, clamp01((t - shots[0]) / 0.3), 10, 2.4, 8); }] });
  }
  // ================= 16 meanwhile the cork is slowing down... then it stops dead (insert; the hardest hit on "dead")
  const tDead = w("dead,");
  {
    const t0 = w("Meanwhile,"), t1 = w("just", w("dead,"));
    const tSlow = w("slowing");
    const X0 = 8;   // somewhere astern of him by now
    const cx = (t: number) => { const u = clamp01((t - tSlow) / (tDead - tSlow)); return X0 - 0.75 * (Math.min(t, tSlow) - t0) - 0.75 * (tDead - tSlow) * (u - u * u / 2); };
    const corkP = (t: number): V3 => [cx(t), 0.08, CORK0[2]];
    const key = (t: number, near: number, extra: Partial<CamKey> = {}): CamKey => { const c = corkP(t); return { t, pos: [c[0] + 1.6 * near, 1.3 * near, c[2] + 3.6 * near], look: [c[0] - 0.2, 0.2, c[2]], fov: 42, ...extra }; };
    add({ id: "corkslow", place: "water", insert: true, t0, t1, xfade: 0.2, join: { kind: "dissolve", frames: 6, match: true }, set: () => straitSet(), light: "golden", lens: { cInf: 9 },
      cam: [{ ...key(t0, 1), drift: 0 }, { ...key(tDead - 0.02, 1.05), glide: 1 }, { ...key(tDead + 0.1, 0.62), sharp: true }, { ...key(t1, 0.6), glide: 1 }],
      people: [],
      rigs: [currentRig((t) => -0.75 * Math.min(t, tDead), (t) => 1 - 0.85 * clamp01((t - tSlow) / (tDead - tSlow))), corkRig(corkP), glints([{ at: [cx(tDead), 0.7, CORK0[2]], t: tDead, size: 1.2 }])] });
  }
  // ================= 17 just as the enemy flagship pulls close enough to spit on (alongside his bow)
  const JF: Berth = { x: 31, z: 7.4, yaw: Math.PI, k: 3 };
  {
    const t0 = w("just", tDead), t1 = w("You");
    const slide = (t: number) => 3 * (1 - sm((t - t0) / (w("close", t0) - t0 + 0.3)));
    const EA = (t: number) => onDeck({ ...JF, x: JF.x + slide(t) }, 6.4, 1.6, DECK_J);
    const A2 = onDeck(FLAG, 8.0, 2.6, DECK_K);
    add({ id: "spit", place: "bow", t0, t1, xfade: 0, join: { kind: "cut" }, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [pair(t0, [A2, EA(t0), EA(t1)], -20, 6, 42, 0), { ...pair(t1, [A2, EA(t0), EA(t1)], -10, 6, 38, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => A2, faceTo: () => EA(t1), props: () => admProps(faceTrack(words, "deadpan", [], t0), "hold") },
        { id: "ea", at: EA, faceTo: () => A2, props: () => ({ costume: "samurai2", seed: 71, face: faceTrack(words, "cackle", [{ word: "spit", face: "angry", react: [{ face: "squeeze", frames: 2 }] }], t0), pose: poseTrack(words, "point", [["spit", "strikeUp"]], t0) }) }],
      rigs: [currentRig(() => 0, () => 0.15), fleetRig((b) => korean(b.k === 0, true), MINE), fleetRig((b) => japanese(b.k), [JF], (t) => ({ dx: slide(t) })), fleetRig((b) => japanese(b.k), FRONT.slice(3, 20))] });
  }
  // ================= 18 you see: some narrow sea channels run like a river, and every few hours stop and turn around
  {
    const t0 = w("You"), t1 = w("Now");
    const tTurns = w("turns"), tStop = w("stops", t0);
    // water speed: -9 m/s, easing to slack from "stops" to "turns", then easing up to +9 m/s; the phase is its integral
    const vel = (t: number) => (t < tTurns ? -9 * (1 - sm((t - tStop) / (tTurns - tStop))) : 9 * sm((t - tTurns) / 0.5));
    const ph = (t: number) => { let p = 0; const dt = 1 / 240; for (let u = t0; u < t; u += dt) p += vel(Math.min(t, u + dt / 2)) * Math.min(dt, t - u); return p; };
    const slack = (t: number) => sm((t - tStop) / (tTurns - tStop)) * (1 - sm((t - tTurns) / 0.5));
    add({ id: "explain", place: "explain", insert: true, t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet({ explain: true, fog: 14 }), light: "explain", lens: { cInf: 2 },
      cam: [{ t: t0, pos: [70, 190, -80], look: [70, 0, 0], fov: 44 }, { t: w("The", t0), pos: [150, 150, -110], look: [72, 0, 0], fov: 44, glide: 1 }, { t: t1, pos: [160, 135, -96], look: [74, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [currentRig(ph, (t) => 1 - 0.8 * slack(t)), arrowsRig((t) => (t < tTurns ? -1 : 1), tTurns),
        label("NARROW SEA CHANNEL", [70, 14, 0], w("narrow", t0), w("The", t0) - 0.1, 7), label("EVERY FEW HOURS", [76, 14, 0], w("every", t0), t1 + 1, 7)] });
  }
  // ================= 19 now the water that rushed them in shoves them back (the jam drifting backwards)
  const tShoves = w("shoves");
  const jam = JB.map((b) => ({ ...b, x: b.x - 26 }));
  const drift = (t: number, b: Berth) => { const u = Math.max(0, t - tShoves); const k = 1 + ((b.k * 37) % 10) / 12; return { dx: 1.6 * u * u * k + 2.2 * u * k, dyaw: ((b.k * 53) % 7 - 3) * 0.08 * Math.min(1, u), heel: ((b.k * 17) % 5 - 2) * 0.03 * Math.min(1, u) }; };
  {
    const t0 = w("Now"), t1 = w("His", tShoves);
    add({ id: "shove", place: "gap", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ fog: 9 }), light: "golden", lens: { cInf: 3 },
      cam: [{ t: t0, pos: [0, 48, 60], look: [70, 0, 0], fov: 44 }, { t: t1, pos: [10, 44, 54], look: [78, 0, 0], fov: 44, glide: 1 }],
      people: [],
      rigs: [currentRig((t) => 6 * t, () => 1), arrowsRig(() => 1, t0 - 1, 0.6), myFleet, fleetRig((b) => japanese(b.k), jam, drift)] });
  }
  // ================= 20 his ships are anchored (he stands easy, the anchor rope taut against the current)
  {
    const t0 = w("His", tShoves), t1 = w("Theirs");
    add({ id: "anchored", place: "mydeck", t0, t1, xfade: 0.2, join: WHIP, set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [cK(t0, [ADM], "medium", -30, 8, 40), { ...cK(t1, [ADM], "medium", -24, 8, 36), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => [ADM[0] + 10, ADM[1], ADM[2]], props: () => admProps(faceTrack(words, "focus", [{ word: "anchored.", face: "smug" }], t0), poseTrack(words, "stand", [["anchored.", "hips"]], t0)) }],
      rigs: [currentRig((t) => 6 * t, () => 1), myFleet, ropeRig(onDeck(FLAG, 9.4, 2.0, DECK_K), [36, 0, 5])] });
  }
  // ================= 21 theirs aren't (an enemy deck sliding backwards, the crew grabbing air) - a match dissolve
  // from 20: the same medium framing, the figure keeps its spot
  {
    const t0 = w("Theirs"), t1 = w("Their", t0);
    const JS: Berth = { x: 60, z: -2, yaw: Math.PI, k: 5 };
    const at = (lx: number, lz: number) => (t: number) => onDeck({ ...JS, x: JS.x + 4 * (t - t0) }, lx, lz, DECK_J);
    const E1 = at(6.2, 0.9), E2 = at(5.4, -1.0);
    add({ id: "theirs", place: "jdeck2", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: "golden", lens: { cInf: 6 },
      cam: [cK(t0, [E1(t0), E2(t0), E1(t1), E2(t1)], "medium", -96, 8, 40), { ...cK(t1, [E1(t0), E2(t0), E1(t1), E2(t1)], "medium", -90, 8, 38), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "e1", at: E1, faceTo: () => [0, DECK_J, 0], props: () => ({ costume: "samurai", seed: 81, face: faceTrack(words, "worried", [{ word: "aren't.", face: "terrified" }], t0), pose: poseTrack(words, "point", [["aren't.", "armsUp"]], t0) }) },
        { id: "e2", at: E2, faceTo: () => [0, DECK_J, 0], props: () => ({ costume: "ashigaru", seed: 82, face: faceTrack(words, "terrified", [{ word: "aren't.", face: "scream" }], t0 + 0.1), pose: "armsUp" }) }],
      rigs: [currentRig((t) => 6 * t, () => 1), fleetRig((b) => japanese(b.k), [JS], (t) => ({ dx: 4 * (t - t0), heel: 0.05 * Math.sin(t * 4) }))] });
  }
  // ================= 22 their front ships pile into the ones behind, and his cannons pound the jam
  {
    const t0 = w("Their", w("Theirs")), t1 = w("By");
    const A: Berth = { x: 70, z: 6, yaw: Math.PI - 0.15, k: 60 }, B2: Berth = { x: 81, z: 3, yaw: Math.PI + 0.25, k: 61 };
    const tHit = w("into", t0) - 0.05, tPound = w("pound"), tJam = w("jam.");
    const mA = (t: number) => ({ dx: 4 * sm((t - t0) / (tHit - t0)), dyaw: 0.5 * sm((t - tHit) / 0.6), heel: t > tHit ? 0.12 * Math.sin((t - tHit) * 6) * Math.exp(-(t - tHit)) : 0 });
    const mB = (t: number) => ({ dx: 1.5 * sm((t - t0) / (tHit - t0)), dyaw: -0.4 * sm((t - tHit) / 0.6), heel: t > tHit ? -0.12 * Math.sin((t - tHit) * 6) * Math.exp(-(t - tHit)) : 0 });
    const crewA = [[2.4, 0.9], [0.2, -1.0]].map(([lx, lz], j): PersonSpec => ({ id: `ca${j}`, at: (t) => { const m = mA(t); return onDeck({ ...A, x: A.x + m.dx, yaw: A.yaw + m.dyaw }, lx, lz, DECK_J); }, faceTo: () => [B2.x, DECK_J, B2.z],
      props: () => ({ costume: j ? "ashigaru" : "samurai", seed: 83 + j, face: faceTrack(words, "worried", [{ word: "into", after: t0, face: "terrified", react: [{ face: "scream", frames: 3 }] }], t0 + j * 0.1), pose: [{ t: t0, v: "point" }, { t: tHit, v: "armsUp" }] }) }));
    const crewLate = [tHit + 0.3, tHit + 0.7, w("and", tHit), tPound, tJam, t1].flatMap((t) => crewA.map((p) => p.at(t)));
    add({ id: "jam", place: "gap-low", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet(), light: lightArc([[t0, "golden"]], [tPound, tJam].map((t) => ({ kind: "flash" as const, t, frames: 2 }))), lens: { cInf: 5 },
      alive: [[t0, t1]],
      cam: [{ t: t0, pos: [61, 18, 34], look: [76, 2, 5], fov: 52, drift: 0.3 }, { t: tHit + 0.35, pos: [61, 17, 32], look: [73.5, 2.5, 5.5], fov: 50, glide: 1 },
        { ...pair(w("and", tHit) + 0.1, crewLate, 30, 14, 50, 0.2), glide: 1 }, { ...pair(t1, crewLate, 26, 14, 50, 0.2), glide: 1 }],
      people: crewA,
      rigs: [currentRig((t) => 5 * t, () => 1), fleetRig((b) => japanese(b.k), [A], (t) => mA(t)), fleetRig((b) => japanese(b.k), [B2], (t) => mB(t)),
        burst([{ at: [78, 3, 4], t: tHit, size: 4 }, { at: [79, 4, 5], t: tHit + 0.25, size: 3 }, { at: [74, 4, 9], t: tPound, size: 4.4 }, { at: [84, 4, 0], t: tJam, size: 5 }]),
        debris([{ at: [78, 3.5, 4], t: tHit, n: 40, kind: "splinter", size: 0.35, floorY: 0.1, up: 5, speed: 4 }, { at: [84, 4, 0], t: tJam, n: 30, kind: "splinter", size: 0.35, floorY: 0.1, up: 6, speed: 4 }])] });
  }
  // ================= 23 by sunset the whole enemy fleet is drifting backwards out of the channel (from astern of him)
  const SUN = DUSK;
  {
    const t0 = w("By"), t1 = w("their", w("By"));
    const back = (t: number, b: Berth) => ({ dx: 14 + 9 * (t - t0) * (1 + ((b.k * 37) % 10) / 20), dyaw: ((b.k * 53) % 7 - 3) * 0.08 });
    add({ id: "sunset", place: "mouth-dusk", establishing: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ dusk: true }), light: SUN, lens: { cInf: 3 },
      cam: [{ t: t0, pos: [20, 45, 30], look: [100, 8, -20], fov: 46, drift: 0 }, { t: t1, pos: [23, 43, 28], look: [101, 8, -20], fov: 46, glide: 1 }],
      people: [],
      rigs: [currentRig((t) => 9 * t, () => 1), myFleet, fleetRig((b) => japanese(b.k), jam, back), wreckRig([[60, -10, 0.4], [76, 12, -0.5]], (i) => japanese(i + 1))] });
  }
  // ================= 24 their admiral close enough to wave goodbye (at his bow, drifting away backwards)
  {
    const t0 = w("their", w("By")), t1 = w("His", t0);
    const JG: Berth = { x: 44, z: 2, yaw: Math.PI, k: 3 };
    const EA = (t: number) => onDeck({ ...JG, x: JG.x + 3 * (t - t0) }, 6.0, 0.4, DECK_J);
    add({ id: "goodbye", place: "jbow-dusk", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ dusk: true }), light: SUN, lens: { cInf: 6 },
      cam: [pair(t0, [EA(t0), EA(t1)], -90, 6, 40, 0), { ...pair(t1, [EA(t0), EA(t1)], -80, 6, 38, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "ea", at: EA, faceTo: () => ADM, props: () => ({ costume: "samurai2", seed: 71, face: faceTrack(words, "stunned", [{ word: "goodbye.", face: "sob" }], t0), pose: poseTrack(words, "stand", [["wave", "sweep"]], t0) }) }],
      rigs: [currentRig((t) => 6 * t, () => 1), fleetRig((b) => japanese(b.k), [JG], (t) => ({ dx: 3 * (t - t0) })), fleetRig((b) => japanese(b.k), jam.slice(6, 30), (t, b) => ({ dx: 40 + 5 * (t - t0) + (b.k % 5) }))] });
  }
  // ================= 25 his captain, who called it parking, now says it was his idea (hand on his chest; he side-eyes)
  {
    const t0 = w("His", w("goodbye.")), t1 = w("And", t0);
    add({ id: "idea", place: "mydeck-dusk", t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ dusk: true }), light: SUN, lens: { cInf: 6 },
      cam: [pair(t0, [ADM, CAP], -20, 6, 40, 0), { ...pair(t1, [ADM, CAP], -12, 6, 36, 0), glide: 1 }], alive: [[t0, t1]],
      people: [{ id: "cap", at: () => CAP, faceTo: () => [CAP[0] - 10, CAP[1], CAP[2]], props: () => capProps(faceTrack(words, "smug", [{ word: "idea.", face: "bliss" }], t0), poseTrack(words, "hips", [["says", "handIn"]], t0)) },
        { id: "adm", at: () => ADM, faceTo: () => CAP, props: () => admProps(faceTrack(words, "deadpan", [{ word: "idea.", face: "blank" }], t0 + 0.13), "stand") }],
      rigs: [currentRig((t) => 6 * t, () => 1), myFleet] });
  }
  // ================= 26 and the cork drifts right back past him, going the other way (at the water by his hull)
  {
    const t0 = w("And", w("idea.")), t1 = END;
    const corkB = (t: number): V3 => [ADM[0] + 2.0 - 1.4 * (t - t0), 0.08, CORK0[2]];
    add({ id: "corkback", place: "water-dusk", insert: true, t0, t1, xfade: 0.2, join: D(6), set: () => straitSet({ dusk: true }), light: SUN, lens: { cInf: 7 },
      cam: [{ t: t0, pos: [ADM[0], 2.0, 13], look: [ADM[0], 2.4, 3], fov: 50, drift: 0 }, { t: t1, pos: [ADM[0], 2.1, 12.5], look: [ADM[0], 2.45, 3], fov: 49, glide: 1 }],
      alive: [[t0, t1]],
      people: [{ id: "adm", at: () => ADM, faceTo: () => [ADM[0], ADM[1], ADM[2] + 10], props: () => admProps(faceTrack(words, "focus", [{ word: "past", face: "sly" }], t0), "hold") }],
      rigs: [currentRig((t) => -1.4 * t, () => 0.6), myFleet, corkRig(corkB)] });
  }
  void DECK_J;
  return { groups };
}
