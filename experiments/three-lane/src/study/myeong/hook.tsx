// HOOK LAB (internal): story-myeongnyang v3's hook built in code to match the Codex reference key frame
// (experiments/asset-gen/gen/kf_myeong_v3.png): an anonymous admiral at the bow of an East Asian warship letting the
// anchor go into a roaring strait at dusk, the enemy fleet pouring in behind with lanterns, sailors laughing.
// It reuses the episode's strait world (src/myeongnyang/sets.ts, read only) and adds the close set in code: the bow deck,
// the painted rail and hull, a carved dragon post (the SDF dragon in lacquer), the anchor with its rope and chain
// mid-drop, the splash, churning water. Pass 3 targets kf_myeong_v4.png (toon): the ship is turned broadside so the drop
// is over open water; the camera is already moving at frame 0 (a slow eased push and rise).
import React from "react";
import * as THREE from "three";
import { Episode3D } from "../../kit/Episode3D";
import type { CapWord } from "../../kit/captions";
import type { GroupSpec, Rig, V3, PersonSpec } from "../../kit/Stage";
import type { CamKey } from "../../kit/campath";
import { lambert, box } from "../../kit/sets";
import { richWater } from "../../kit/dressing";
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

// pass 3 (target kf_myeong_v4.png): turn the ship, not the camera. The camera looks up the strait (+x, the fleet beyond)
// from low over the water. The hero bow lies broadside, turned 10 degrees away from the lens. Its rail faces the lens across
// the lower left at his waist, and he stands just inboard of it. The blunt panokseon bow face ends just past him and
// recedes to the left, so the right of the frame is open water. The anchor goes over the bow corner on its chain and lands
// in the lower right-centre. The deck sits HK above the water: a cartoon cheat, because the real 3.4 m deck puts the water
// under him out of any frame that holds his head at 0.2.
const D2R = Math.PI / 180, HK = 0.35, RAIL = 0.5, RL = 2.4, AZ = -88, EL = 5, FOV = 40, BOW_G = 100;
const ADM: V3 = [18, HK, 0];
const HEAD: V3 = [ADM[0], ADM[1] + 1.375, ADM[2]];
// his head 0.2 of the frame at (0.2, 0.28); a slow push and rise already under way at frame 0 (io from t -0.9), no snap
const CAM0 = frameKey(-0.9, HEAD, 0.2, 0.28, 0.59, 0.2, AZ, EL, FOV, "io"), CAM1 = frameKey(F(110), HEAD, 0.21, 0.29, 0.59, 0.215, AZ + 2, EL + 2.5, FOV - 2, "io");
// the ship's frame: heading = BOW_G degrees from "toward the lens" toward the screen's right; OUT (local +z, the rail side)
// faces the lens
const [HD, OUT] = (() => { const a = AZ * D2R, g = BOW_G * D2R, fx = -Math.sin(a), fz = -Math.cos(a), rx = Math.cos(a), rz = -Math.sin(a);
  const hx = -Math.cos(g) * fx + Math.sin(g) * rx, hz = -Math.cos(g) * fz + Math.sin(g) * rz;
  return [[hx, hz], [-Math.sin(g) * fx - Math.cos(g) * rx, -Math.sin(g) * fz - Math.cos(g) * rz]]; })();
/** ship-local (lx along the keel from the admiral, ly above the deck, lz from the centreline; the rail at lz RL) to world */
const SHIP_O: V3 = [ADM[0] - OUT[0] * (RL - 0.65), HK, ADM[2] - OUT[1] * (RL - 0.65)];
const ship = (lx: number, ly: number, lz: number): V3 => [SHIP_O[0] + HD[0] * lx + OUT[0] * lz, HK + ly, SHIP_O[2] + HD[1] * lx + OUT[1] * lz];
/** his pointing hand in the world: the Actor's "point" pose puts it 240 svg units right of centre and 460 above the feet
 * (PERSON_K 0.0025 m per unit) on a card that faces the camera */
const HAND: V3 = (() => { const c = new THREE.PerspectiveCamera(); c.position.set(...CAM0.pos); c.lookAt(new THREE.Vector3(...CAM0.look)); c.updateMatrixWorld();
  const r = new THREE.Vector3().setFromMatrixColumn(c.matrixWorld, 0); r.y = 0; r.normalize(); return [ADM[0] + r.x * 0.6, ADM[1] + 1.15, ADM[2] + r.z * 0.6]; })();
function rayToWater(k: CamKey, sx: number, sy: number, y = 0.05): V3 {
  const c = new THREE.PerspectiveCamera(k.fov ?? 40, 9 / 16); c.position.set(...k.pos); c.lookAt(new THREE.Vector3(...k.look)); c.updateMatrixWorld();
  const th = Math.tan(((k.fov ?? 40) * Math.PI) / 360), d = new THREE.Vector3((sx - 0.5) * 2 * th * (9 / 16), -(sy - 0.5) * 2 * th, -1).transformDirection(c.matrixWorld);
  const t = (y - c.position.y) / d.y; return [c.position.x + d.x * t, y, c.position.z + d.z * t];
}
// the splash is where the first key's screen ray (0.78, 0.86) meets the water. The bow face (from the rail corner at
// BOW_X, raked 0.3 forward to the centreline) ends 0.5 m short of it in ship x, so the drop is over open water and never
// behind the hull.
const SPLASH: V3 = rayToWater(CAM0, 0.82, 0.68);   // further out, so the drop reads whole and smaller
const SPLASH_L = [(SPLASH[0] - SHIP_O[0]) * HD[0] + (SPLASH[2] - SHIP_O[2]) * HD[1], (SPLASH[0] - SHIP_O[0]) * OUT[0] + (SPLASH[2] - SHIP_O[2]) * OUT[1]];
const BOW_X = Math.min(0.7, SPLASH_L[0] - 0.5 - (0.3 * (RL - Math.min(SPLASH_L[1], RL))) / RL);
const ANCHOR_K = 0.75;   // the anchor drawn large, as on the reference (1.3 crowded the lens at frame 0)
const LEAD = F(16);     // the drop is already under way at frame 0, so the anchor starts out over the water, not in front of the lens
// the anchor starts out to his right on screen (never between the lens and him), then falls to the splash
const ANCHOR0: V3 = [SPLASH[0], SPLASH[1] + 1.6, SPLASH[2]];   // straight above the splash, so it falls on his right
const T_HIT = F(34);

function bowSet() {
  const s = straitSet({ dusk: true });
  const root = s.root;
  // pass 3: the hero bow in its own frame (see ship()); aft runs off the left edge. Flat toon colours, as on v4
  const hero = new THREE.Group(); hero.matrixAutoUpdate = false; root.add(hero);
  hero.matrix.makeBasis(new THREE.Vector3(HD[0], 0, HD[1]), new THREE.Vector3(0, 1, 0), new THREE.Vector3(OUT[0], 0, OUT[1])).setPosition(SHIP_O[0], HK, SHIP_O[2]);
  const AFT = -10, L = BOW_X - AFT, MX = (AFT + BOW_X) / 2, HH = HK + 0.6;
  const deckM = lambert({ color: "#b07a48" }), blue = lambert({ color: "#3b56a0" }), brown = lambert({ color: "#7a4a2a" }), red = lambert({ color: "#c8382c" }), gold = lambert({ color: "#e8b040" });
  box(hero, deckM, L, 0.25, 2 * RL, MX, -0.12, 0);                                              // the deck
  box(hero, blue, L, 0.42, 0.3, MX, -0.2, RL + 0.12); box(hero, gold, L, 0.08, 0.32, MX, -0.44, RL + 0.12);   // blue planks, gold trim
  box(hero, brown, L, HH - 0.48, 0.3, MX, -0.48 - (HH - 0.48) / 2, RL + 0.1);                  // the lower hull
  // the blunt panokseon bow face, raked 0.3 forward at the centreline (two angled panels)
  for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.3, HH + 0.4, Math.hypot(RL, 0.3)), blue); p.position.set(BOW_X + 0.15, -HH / 2 + 0.2, s * RL / 2); p.rotation.y = s * Math.atan2(0.3, RL); hero.add(p); }
  for (let x = AFT; x <= BOW_X + 0.01; x += 1.1) box(hero, red, 0.09, RAIL + 0.05, 0.09, x, RAIL / 2, RL);   // rail posts (thin: they sit beside the lens)
  box(hero, red, L + 0.2, 0.16, 0.26, MX, RAIL, RL); box(hero, red, L, 0.1, 0.14, MX, RAIL * 0.45, RL);
  box(hero, red, 0.12, 0.08, 2 * RL, BOW_X, RAIL, 0); box(hero, red, 0.12, RAIL + 0.2, 0.12, BOW_X, (RAIL + 0.2) / 2, RL);   // the bow rail and corner post
  // the carved dragon prow on the bow's lens side (the SDF dragon in red lacquer), looking out over the water
  const post = sdfDragon({ mat: lambert({ color: "#c8352a" }), whiskers: true }); post.scale.setScalar(0.55); post.position.set(BOW_X - 0.7, -0.15, RL + 0.35); post.rotation.y = 0; hero.add(post);
  // the mast and a furled-sail edge behind him (top left, as on v4)
  const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.15, 9, 10), brown); mast.position.set(-2.2, 4.5, 0); hero.add(mast);
  box(hero, lambert({ color: "#efe2c4" }), 0.08, 4.5, 3.2, -2.3, 5.2, 0.2);
  // dusk water: deep and dark under the strait's bright streaks
  const dark = new THREE.Mesh(new THREE.PlaneGeometry(700, 700), lambert({ map: richWater([60, 60], { deep: true }) })); dark.rotation.x = -Math.PI / 2; dark.position.set(100, 0.02, 0); dark.receiveShadow = true; root.add(dark);
  // coiled rope near the admiral
  const coil = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.1, 10, 28), lambert({ color: "#d0a868" })); coil.rotation.x = Math.PI / 2; coil.position.set(-1.2, 0.1, 1.2); hero.add(coil);
  // pass 3: a smooth dusk sky as on v4 (violet zenith, magenta, orange at the horizon) with a few soft lit clouds
  const sc = document.createElement("canvas"); sc.width = 64; sc.height = 1024; const sg = sc.getContext("2d")!;
  const grd = sg.createLinearGradient(0, 0, 0, 1024); grd.addColorStop(0, "#3a2a7a"); grd.addColorStop(0.3, "#6a3a9a"); grd.addColorStop(0.4, "#b8508a"); grd.addColorStop(0.47, "#f07a4a"); grd.addColorStop(0.52, "#f8a860"); grd.addColorStop(1, "#3a3050");
  sg.fillStyle = grd; sg.fillRect(0, 0, 64, 1024);
  const sky = (s as unknown as { sky?: THREE.Mesh }).sky;
  if (sky) { const W = 2048, Hh = 1024, [cc, cg] = (() => { const c2 = document.createElement("canvas"); c2.width = W; c2.height = Hh; return [c2, c2.getContext("2d")!] as const; })();
    cg.drawImage(sc, 0, 0, W, Hh);
    let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
    for (let k = 0; k < 7; k++) { const y = Hh * (0.3 + rnd() * 0.12), x = rnd() * W, w = 160 + rnd() * 200, h = 14 + rnd() * 10;
      for (let j = 0; j < 4; j++) { const ox = (j - 1.5) * w * 0.22, r = h * (1 + (j % 2) * 0.5);
        cg.fillStyle = "rgba(240,150,140,0.95)"; cg.beginPath(); cg.ellipse(x + ox, y - r * 0.3, w * 0.2, r, 0, 0, 7); cg.fill(); }
      cg.fillStyle = "rgba(255,190,120,0.95)"; cg.beginPath(); cg.ellipse(x, y + h * 0.4, w * 0.45, h * 0.45, 0, 0, 7); cg.fill(); }
    const tx = new THREE.CanvasTexture(cc); tx.colorSpace = THREE.SRGBColorSpace; (sky.material as THREE.MeshBasicMaterial).map = tx; (sky.material as THREE.MeshBasicMaterial).needsUpdate = true; }
  // (5) sculpted rock cliffs with pines on both shores of the strait ahead: noise-displaced columns, ledges, pine cones
  const rock = lambert({ color: "#6a5a62" }), rockLit = lambert({ color: "#8a7470" }), pine = lambert({ color: "#2f4a3a" });
  let rs = 11; const rr = () => ((rs = (rs * 16807) % 2147483647) / 2147483647);
  for (const side of [-1, 1]) for (let k = 0; k < 9; k++) {
    const x = 45 + k * 14 + rr() * 6, z = side * (34 + rr() * 10 + (k > 5 ? 12 : 0)), h = 28 + rr() * 26, r0 = 7 + rr() * 5;
    const geo = new THREE.CylinderGeometry(r0 * 0.7, r0, h, 14, 8), p = geo.getAttribute("position") as THREE.BufferAttribute;
    for (let i = 0; i < p.count; i++) { const a = Math.atan2(p.getZ(i), p.getX(i)), y = p.getY(i), n = 1 + 0.18 * Math.sin(a * 5 + y * 0.4 + k) + 0.1 * Math.sin(a * 11 - y * 0.9) + (Math.round(y / 4) % 2 ? 0.05 : -0.05);
      p.setX(i, p.getX(i) * n); p.setZ(i, p.getZ(i) * n); }
    geo.computeVertexNormals();
    const cl = new THREE.Mesh(geo, k % 2 ? rock : rockLit); cl.position.set(x, h / 2 - 2, z); cl.castShadow = true; cl.receiveShadow = true; root.add(cl);
    for (let q = 0; q < 6; q++) { const ph = 3 + rr() * 4, pn = new THREE.Mesh(new THREE.ConeGeometry(ph * 0.35, ph, 7), pine); const a = rr() * Math.PI * 2, rad = r0 * 0.6 * rr();
      pn.position.set(x + Math.cos(a) * rad, h - 2 + ph / 2 - 0.5, z + Math.sin(a) * rad); root.add(pn); }
  }
  return s;
}

/** (4) foam crests: white curling crest patches drifting with the current over the near water and up the strait */
const foamCrests = (n = 260): Rig => (ctx) => {
  const c = document.createElement("canvas"); c.width = 128; c.height = 64; const g = c.getContext("2d")!;
  g.strokeStyle = "rgba(250,253,255,0.95)"; g.lineWidth = 6; g.lineCap = "round"; g.beginPath(); g.moveTo(8, 44); g.quadraticCurveTo(50, 8, 96, 30); g.quadraticCurveTo(110, 38, 104, 48); g.stroke();
  g.fillStyle = "rgba(250,253,255,0.8)"; for (let k = 0; k < 14; k++) { g.beginPath(); g.arc(30 + Math.random() * 80, 20 + Math.random() * 30, 2 + Math.random() * 4, 0, 7); g.fill(); }
  const tex = new THREE.CanvasTexture(c); tex.colorSpace = THREE.SRGBColorSpace;
  const mat = new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false, fog: true });
  const geo = new THREE.PlaneGeometry(1, 0.5); geo.rotateX(-Math.PI / 2);
  const im = new THREE.InstancedMesh(geo, mat, n); im.layers.set(NOINK); im.renderOrder = 4; ctx.root.add(im);
  let seed = 3; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  const base = Array.from({ length: n }, (_, i) => { const near = i < n * 0.45; return { x: near ? 12 + rnd() * 22 : 30 + rnd() * 110, z: near ? 2 + rnd() * 14 : -30 + rnd() * 60, s: near ? 1.4 + rnd() * 1.6 : 3 + rnd() * 5, r: rnd() * 0.6 - 0.3, ph: rnd() * 6 }; });
  const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), sc = new THREE.Vector3(), pos = new THREE.Vector3();
  return (t) => { base.forEach((b, i) => { const x = ((b.x - 7 * t - 10) % 130 + 130) % 130 + 10; const k = 0.6 + 0.4 * Math.sin(t * 3 + b.ph);
      pos.set(x, 0.09, b.z); q.setFromAxisAngle(new THREE.Vector3(0, 1, 0), b.r); sc.set(b.s * k, 1, b.s * k); m4.compose(pos, q, sc); im.setMatrixAt(i, m4); }); im.instanceMatrix.needsUpdate = true; };
};

/** the anchor (wood and iron) dropping from the rail into the water on its rope and chain, with a splash */
const anchorRig = (): Rig => (ctx) => {
  // pass 3: chunky toon anchor (flat wood and dark iron), drawn ANCHOR_K large, its flukes square to the lens
  const g = new THREE.Group(), wood = lambert({ color: "#9a6236" }), iron = lambert({ color: "#4a4552" });
  box(g, wood, 0.24, 1.6, 0.24, 0, 0, 0); box(g, iron, 0.3, 0.16, 0.3, 0, 0.35, 0); box(g, wood, 1.3, 0.2, 0.2, 0, 0.6, 0);   // shank, iron band, stock
  for (const s of [-1, 1]) { const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.1, 0.9, 8), iron); arm.position.set(s * 0.32, -0.7, 0); arm.rotation.z = s * 0.9; g.add(arm);
    const fl = new THREE.Mesh(new THREE.ConeGeometry(0.18, 0.4, 4), iron); fl.position.set(s * 0.62, -0.45, 0); fl.rotation.z = s * 0.2; g.add(fl); }
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.14, 0.04, 8, 16), iron); ring.position.y = 0.92; g.add(ring);
  g.scale.setScalar(ANCHOR_K); g.traverse((o) => { if ((o as THREE.Mesh).isMesh) o.castShadow = true; }); ctx.root.add(g);
  const links = Array.from({ length: 34 }, () => { const l = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.03, 6, 14), iron); l.scale.set(1.3, 1, 1); l.castShadow = true; ctx.root.add(l); return l; });
  const ropeMat = lambert({ color: "#d8b070" }); let rope: THREE.Mesh | null = null;
  const A = new THREE.Vector3(...ANCHOR0), H = new THREE.Vector3(...HAND), S = new THREE.Vector3(...SPLASH), X = new THREE.Vector3(1, 0, 0);
  const yaw = Math.atan2(CAM0.pos[0] - S.x, CAM0.pos[2] - S.z);   // the anchor's face (local +z) toward the lens
  const spray = burst([{ at: SPLASH, t: T_HIT, size: 2.2, n: 18 }])(ctx);
  const drops = Array.from({ length: 48 }, (_, i) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.06 + (i % 3) * 0.035, 6, 5), new THREE.MeshBasicMaterial({ color: "#f4fbff" })); m.layers.set(NOINK); ctx.root.add(m); return m; });
  const foam = new THREE.Mesh(new THREE.RingGeometry(0.2, 1, 40), new THREE.MeshBasicMaterial({ color: "#f4fbff", transparent: true, depthWrite: false })); foam.rotation.x = -Math.PI / 2; foam.position.set(SPLASH[0], 0.08, SPLASH[2]); foam.layers.set(NOINK); ctx.root.add(foam);
  return (t, cam) => {
    // the drop: off the bow corner and out, falling with gravity to the water by T_HIT, then sinking slowly in the foam
    const u = Math.min(1, Math.max(0, (t + LEAD) / (T_HIT + LEAD))), p = A.clone().lerp(S, Math.min(1, u * 1.3)); p.y = A.y + (S.y - 0.35 - A.y) * u * u;
    if (t > T_HIT) p.y = S.y - 0.35 - (t - T_HIT) * 0.45;
    g.position.copy(p); g.rotation.set(0.12 * Math.sin(t * 2.2), yaw, 0.25 - u * 0.3 + 0.05 * Math.sin(t * 3));
    // the rope from his hand arcs out and down, then the chain hangs on to the anchor ring (rebuilt each frame)
    const top = new THREE.Vector3(0, 0.92 * ANCHOR_K, 0).applyEuler(g.rotation).add(p);
    const curve = new THREE.CatmullRomCurve3([H, H.clone().lerp(top, 0.3).add(new THREE.Vector3(0, 0.05, 0)), H.clone().lerp(top, 0.65).add(new THREE.Vector3(0, -0.12, 0)), top]);
    const len = curve.getLength(), k0 = 0.4, step = 0.17 / len;
    links.forEach((l, i) => { const k = k0 + i * step; l.visible = k <= 1; if (!l.visible) return;
      l.position.copy(curve.getPointAt(k)); l.quaternion.setFromUnitVectors(X, curve.getTangentAt(k)); if (i % 2) l.rotateX(Math.PI / 2); });
    if (rope) { ctx.root.remove(rope); rope.geometry.dispose(); }
    rope = taperTube(new THREE.CatmullRomCurve3(Array.from({ length: 12 }, (_, i) => curve.getPointAt((i / 11) * k0))), () => 0.045, 24, 6, ropeMat); rope.castShadow = true; ctx.root.add(rope);
    spray(t, cam);
    const ts = t - T_HIT;
    drops.forEach((d, i) => { const a = (i / drops.length) * Math.PI * 2, sp = 1.4 + (i % 5) * 0.45, up = 3.0 + (i % 7) * 0.55;
      d.visible = ts > 0 && ts < 1.5; if (!d.visible) return;
      d.position.set(S.x + Math.cos(a) * sp * ts, S.y + up * ts - 4.9 * ts * ts, S.z + Math.sin(a) * sp * ts * 0.7); });
    foam.visible = ts > 0; if (ts > 0) { const r = 0.7 + ts * 1.8; foam.scale.setScalar(r); (foam.material as THREE.MeshBasicMaterial).opacity = Math.max(0, 0.9 - ts * 0.3); }
  };
};

export function buildHook(): { groups: GroupSpec[] } {
  const fleet = japaneseFleet(46, 40);   // pass 3: the fleet starts nearer, so the nearest ship reads big (v4)
  // the enemy pours in: the fleet slides toward the strait's mouth, the near ships fastest
  const move = (t: number, b: { x: number; k: number }) => ({ dx: -(2.4 + 0.02 * (120 - b.x)) * t });
  const near = fleet.slice(0, 3), lanterns = fleet.slice(0, 18).flatMap((b) => [onDeck(b, 2, 2.4, DECK_K + 2.2), onDeck(b, -3, -2.2, DECK_K + 2.6)]);
  const laughers: PersonSpec[] = near.flatMap((b, i) => [0, 1].map((j) => ({ id: `jp${i}${j}`, extra: true, scale: 1, at: (t: number) => { const p = onDeck(b, 1 - j * 2.2, (j - 0.5) * 2.4, DECK_K - 0.2); return [p[0] + move(t, b).dx, p[1], p[2]] as V3; }, faceTo: () => ADM,
    props: () => ({ costume: j ? "ashigaru" : "samurai", seed: 30 + i * 2 + j, face: [{ t: 0, v: "grin" }, { t: 0.3 + i * 0.2, v: "cackle" }], pose: [{ t: 0, v: j ? "point" : "laugh" }], blinks: [] }) })));
  // framed by subject (kit frameKey, see CAM0/CAM1): the rail across the lower left, the anchor drop on the right
  const cam: CamKey[] = [CAM0, CAM1];
  return { groups: [{
    id: "hook", place: "bow", t0: 0, t1: F(110), xfade: 0, set: bowSet, light: "golden", env: "day", lens: { cInf: 6 }, cam,
    people: [{ id: "admiral", at: () => ADM, faceTo: () => HAND, props: () => ({ costume: "yi", seed: 13, face: [{ t: 0, v: "focus" }], pose: [{ t: 0, v: "point" }], blinks: [] }) }, ...laughers],
    rigs: [currentRig((t) => 6 * t, () => 1), fleetRig((b) => japanese(b.k), fleet, move), lanternGlows(lanterns, 2.4), bokeh(lanterns, { color: "#ffb860", k: 4 }), anchorRig(), foamCrests()],
    alive: [[0, F(110)]], clouds: false,
  } as GroupSpec] };
}

export const MyeongHook: React.FC = () => (
  <Episode3D words={WORDS} durations={[110 / 30]} build={buildHook} captions="ricks-phrase" gates="off" />
);
