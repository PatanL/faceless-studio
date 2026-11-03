// HOOK LAB (internal): story-myeongnyang v3's hook built in code to match the Codex reference key frame
// (experiments/asset-gen/gen/kf_myeong_v3.png): an anonymous admiral at the bow of an East Asian warship letting the
// anchor go into a roaring strait at dusk, the enemy fleet pouring in behind with lanterns, sailors laughing.
// It reuses the episode's strait world (src/myeongnyang/sets.ts, read only) and adds the close set in code: the bow deck,
// the painted rail and hull, a carved dragon post (the SDF dragon in lacquer), the anchor with its rope and chain
// mid-drop, the splash, churning water. The camera is already moving at frame 0 (a slow push and rise past the rail).
import React from "react";
import * as THREE from "three";
import { Episode3D } from "../../kit/Episode3D";
import type { CapWord } from "../../kit/captions";
import type { GroupSpec, Rig, V3, PersonSpec } from "../../kit/Stage";
import type { CamKey } from "../../kit/campath";
import { lambert, box } from "../../kit/sets";
import { grainPlanks, richWater } from "../../kit/dressing";
import { glaze, metal } from "../../kit/materials";
import { sdfDragon } from "../../kit/codemodels";
import { taperTube } from "../../kit/heroprops";
import { burst } from "../../kit/fx2";
import { bokeh } from "../../kit/depth";
import { frameKey } from "../../kit/framing";
import { NOINK } from "../../ink";
import { straitSet, currentRig, fleetRig, japanese, japaneseFleet, lanternGlows, onDeck, DECK_K } from "../../myeongnyang/sets";

const F = (f: number) => f / 30;
const WORDS: (CapWord & { br: boolean })[] = [[0, "He anchored"], [22, "his last ships"], [48, "in a roaring"], [70, "strait,"], [92, "with an enemy fleet"]]
  .map(([f, text], i, a) => ({ text: text as string, start: (f as number) / 30, end: ((a[i + 1]?.[0] as number) ?? 110) / 30, br: true }));

// the hero ship's bow: deck top at DECK_K, bow toward +x, the rail on +z; the admiral at the rail
const ADM: V3 = [18.2, DECK_K, 2.15];
const HAND: V3 = [18.95, DECK_K + 1.45, 2.95];
// the camera's first key (framed on his head) - the splash point is where the screen ray (0.72, 0.8) meets the water,
// so the anchor drops into the lower right of the frame as in the reference
const HEAD: V3 = [ADM[0], ADM[1] + 1.375, ADM[2]];
const CAM0 = frameKey(-0.6, HEAD, 0.2, 0.3, 0.59, 0.15, -86, 12, 62, "lin"), CAM1 = frameKey(F(105), HEAD, 0.21, 0.31, 0.59, 0.17, -88, 14, 60, "lin");   // looking forward along the outside of the hull
function rayToWater(k: CamKey, sx: number, sy: number, y = 0.05): V3 {
  const c = new THREE.PerspectiveCamera(k.fov ?? 40, 9 / 16); c.position.set(...k.pos); c.lookAt(new THREE.Vector3(...k.look)); c.updateMatrixWorld();
  const th = Math.tan(((k.fov ?? 40) * Math.PI) / 360), d = new THREE.Vector3((sx - 0.5) * 2 * th * (9 / 16), -(sy - 0.5) * 2 * th, -1).transformDirection(c.matrixWorld);
  const t = (y - c.position.y) / d.y; return [c.position.x + d.x * t, y, c.position.z + d.z * t];
}
const SPLASH: V3 = rayToWater(CAM0, 0.74, 0.8);
const ANCHOR0: V3 = [SPLASH[0] - 0.4, DECK_K + 0.5, Math.max(3.3, SPLASH[2] - 1.0)];
const T_HIT = F(34);

function bowSet() {
  const s = straitSet({ dusk: true });
  const root = s.root;
  const planks = lambert({ map: grainPlanks([3, 6], { hue: 26, light: 46, boards: 8, seed: 5 }) });
  // painted hull planks: red with a blue band and gold trim, as on the reference
  const c = document.createElement("canvas"); c.width = 256; c.height = 256; const g = c.getContext("2d")!;
  g.fillStyle = "#9a2a22"; g.fillRect(0, 0, 256, 256); g.fillStyle = "#2a4a8a"; g.fillRect(0, 150, 256, 46); g.fillStyle = "#e0a840"; g.fillRect(0, 144, 256, 6); g.fillRect(0, 196, 256, 6);
  for (let y = 0; y < 256; y += 24) { g.fillStyle = "rgba(0,0,0,0.25)"; g.fillRect(0, y, 256, 2); }
  for (let x = 20; x < 256; x += 64) { g.fillStyle = "#e0a840"; g.beginPath(); g.arc(x, 173, 9, 0, 7); g.fill(); }
  const hullTex = new THREE.CanvasTexture(c); hullTex.colorSpace = THREE.SRGBColorSpace; hullTex.wrapS = hullTex.wrapT = THREE.RepeatWrapping; hullTex.repeat.set(6, 1);
  const hull = lambert({ map: hullTex }), wood = lambert({ map: grainPlanks([1, 1], { hue: 22, light: 36, seed: 7 }) }), red = lambert({ color: "#a8302a" });
  box(root, planks, 13, 0.25, 5.6, 14.5, DECK_K - 0.12, 0);                                 // the deck
  box(root, hull, 13, 3.2, 0.3, 14.5, DECK_K - 1.7, 2.95);                                   // the hull side under the rail
  const bowW = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 2.9, 3.2, 3, 1), hull); bowW.rotation.z = -Math.PI / 2; bowW.rotation.x = Math.PI / 6; bowW.position.set(22.6, DECK_K - 1.6, 0); root.add(bowW);
  for (let x = 9; x <= 21; x += 0.9) box(root, wood, 0.16, 1.1, 0.16, x, DECK_K + 0.55, 2.8);  // rail posts
  box(root, red, 12.4, 0.18, 0.24, 15, DECK_K + 1.12, 2.8); box(root, wood, 12.4, 0.12, 0.14, 15, DECK_K + 0.55, 2.8);
  for (let x = 9.2; x <= 20.8; x += 1.8) box(root, red, 1.2, 0.4, 0.06, x + 0.45, DECK_K + 0.3, 2.86);   // painted panels between posts
  // the carved dragon post at the bow corner (the SDF dragon in red-and-gold lacquer)
  // the carved dragon post stands at the bow, ahead of him (the SDF dragon in red lacquer)
  const post = sdfDragon({ mat: glaze("#c0392b", { rough: 0.35 }), whiskers: true }); post.scale.setScalar(0.8); post.position.set(22.0, DECK_K + 1.2, 1.6); post.rotation.y = Math.PI / 2; root.add(post);
  box(root, wood, 0.3, 1.5, 0.3, 22.0, DECK_K + 0.5, 1.6);
  // dusk water: deep and dark under the strait's bright streaks
  const dark = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), lambert({ map: richWater([60, 60], { deep: true }) })); dark.rotation.x = -Math.PI / 2; dark.position.set(100, 0.02, 0); dark.receiveShadow = true; root.add(dark);
  // coiled rope and a capstan near the admiral
  const coil = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.1, 10, 28), lambert({ color: "#b8956a" })); coil.rotation.x = Math.PI / 2; coil.position.set(15.2, DECK_K + 0.1, 2.0); root.add(coil);
  return s;
}

/** the anchor (wood and iron) dropping from the rail into the water on its rope and chain, with a splash */
const anchorRig = (): Rig => (ctx) => {
  const g = new THREE.Group(), wood = lambert({ map: grainPlanks([1, 1], { hue: 24, light: 38, seed: 3 }) }), iron = metal("iron", { rivets: true });
  box(g, wood, 0.2, 1.6, 0.2, 0, 0, 0); box(g, wood, 1.3, 0.18, 0.18, 0, 0.55, 0);           // shank and stock
  for (const s of [-1, 1]) { const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.09, 0.9, 8), iron); arm.position.set(s * 0.32, -0.7, 0); arm.rotation.z = s * 0.9; g.add(arm);
    const fl = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.36, 4), iron); fl.position.set(s * 0.62, -0.45, 0); fl.rotation.z = s * 0.2; g.add(fl); }
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.12, 0.03, 8, 16), iron); ring.position.y = 0.88; g.add(ring);
  g.traverse((o) => { if ((o as THREE.Mesh).isMesh) o.castShadow = true; }); ctx.root.add(g);
  const links = Array.from({ length: 16 }, (_, i) => { const l = new THREE.Mesh(new THREE.TorusGeometry(0.07, 0.022, 6, 14), iron); l.castShadow = true; ctx.root.add(l); return l; });
  const ropeMat = lambert({ color: "#c8a46a" }); let rope: THREE.Mesh | null = null;
  const A = new THREE.Vector3(...ANCHOR0), H = new THREE.Vector3(...HAND), S = new THREE.Vector3(...SPLASH);
  const spray = burst([{ at: SPLASH, t: T_HIT, size: 1.6, n: 14 }])(ctx);
  const drops = Array.from({ length: 40 }, (_, i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.05 + (i % 3) * 0.03, 6, 5), new THREE.MeshBasicMaterial({ color: "#f4fbff" })); m.layers.set(NOINK); ctx.root.add(m); return m; });
  const foam = new THREE.Mesh(new THREE.RingGeometry(0.2, 1, 40), new THREE.MeshBasicMaterial({ color: "#f4fbff", transparent: true, depthWrite: false })); foam.rotation.x = -Math.PI / 2; foam.position.set(SPLASH[0], 0.08, SPLASH[2]); foam.layers.set(NOINK); ctx.root.add(foam);
  return (t, cam) => {
    // the drop: a short tilt off the rail, then a fall with gravity to the water by T_HIT, then it sinks
    const u = Math.min(1, Math.max(0, t / T_HIT)), p = A.clone().lerp(S, u); p.y = A.y + (S.y - 0.3 - A.y) * u * u;
    if (t > T_HIT) p.y = S.y - 0.3 - (t - T_HIT) * 1.4;
    g.position.copy(p); g.rotation.set(0.2, 0.4, 0.15 + u * 0.5);
    // the chain from the anchor ring up toward the rail, then the rope to his hand (rebuilt each frame)
    const top = p.clone().add(new THREE.Vector3(0, 0.95, 0)), mid = A.clone().add(new THREE.Vector3(0.1, 0.5, -0.2));
    links.forEach((l, i) => { const k = i / (links.length - 1); l.position.copy(top).lerp(mid, k * 0.6); l.rotation.set(i % 2 ? Math.PI / 2 : 0, 0, 0.3); });
    if (rope) { ctx.root.remove(rope); rope.geometry.dispose(); }
    const sag = top.clone().lerp(mid, 0.6).lerp(H, 0.5).add(new THREE.Vector3(0, -0.25, 0.2));
    rope = taperTube(new THREE.CatmullRomCurve3([top.clone().lerp(mid, 0.6), sag, H]), () => 0.035, 24, 6, ropeMat); rope.castShadow = true; ctx.root.add(rope);
    spray(t, cam);
    const ts = t - T_HIT;
    drops.forEach((d, i) => { const a = (i / drops.length) * Math.PI * 2, sp = 1.6 + (i % 5) * 0.5, up = 3.2 + (i % 7) * 0.6;
      d.visible = ts > 0 && ts < 1.4; if (!d.visible) return;
      d.position.set(S.x + Math.cos(a) * sp * ts, S.y + up * ts - 4.9 * ts * ts, S.z + Math.sin(a) * sp * ts * 0.7); });
    foam.visible = ts > 0; if (ts > 0) { const r = 0.6 + ts * 2.2; foam.scale.setScalar(r); (foam.material as THREE.MeshBasicMaterial).opacity = Math.max(0, 0.85 - ts * 0.35); }
  };
};

export function buildHook(): { groups: GroupSpec[] } {
  const fleet = japaneseFleet(72, 40);
  // the enemy pours in: the fleet slides toward the strait's mouth, the near ships fastest
  const move = (t: number, b: { x: number; k: number }) => ({ dx: -(2.4 + 0.02 * (120 - b.x)) * t });
  const near = fleet.slice(0, 3), lanterns = fleet.slice(0, 18).flatMap((b) => [onDeck(b, 2, 2.4, DECK_K + 2.2), onDeck(b, -3, -2.2, DECK_K + 2.6)]);
  const laughers: PersonSpec[] = near.flatMap((b, i) => [0, 1].map((j) => ({ id: `jp${i}${j}`, extra: true, scale: 1, at: (t: number) => { const p = onDeck(b, 1 - j * 2.2, (j - 0.5) * 2.4, DECK_K - 0.2); return [p[0] + move(t, b).dx, p[1], p[2]] as V3; }, faceTo: () => ADM,
    props: () => ({ costume: j ? "ashigaru" : "samurai", seed: 30 + i * 2 + j, face: [{ t: 0, v: "grin" }, { t: 0.3 + i * 0.2, v: "cackle" }], pose: [{ t: 0, v: j ? "point" : "laugh" }], blinks: [] }) })));
  // framed by subject, size and screen spot (kit frameKey): his head ~0.18 of the frame at (0.3, 0.3), from just outboard
  // of the rail and above it, the water and the anchor on the right, the fleet beyond; a slow push and rise under way
  const cam: CamKey[] = [CAM0, CAM1];
  return { groups: [{
    id: "hook", place: "bow", t0: 0, t1: F(110), xfade: 0, set: bowSet, light: "golden", env: "day", lens: { cInf: 6 }, cam,
    people: [{ id: "admiral", at: () => ADM, faceTo: () => HAND, props: () => ({ costume: "yi", seed: 13, face: [{ t: 0, v: "focus" }], pose: [{ t: 0, v: "point" }], blinks: [] }) }, ...laughers],
    rigs: [currentRig((t) => 6 * t, () => 1), fleetRig((b) => japanese(b.k), fleet, move), lanternGlows(lanterns, 2.4), bokeh(lanterns, { color: "#ffb860", k: 4 }), anchorRig()],
    alive: [[0, F(110)]],
  } as GroupSpec] };
}

export const MyeongHook: React.FC = () => (
  <Episode3D words={WORDS} durations={[110 / 30]} build={buildHook} captions="ricks-phrase" gates="off" />
);
