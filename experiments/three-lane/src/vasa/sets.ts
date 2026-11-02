// The places of story-vasa as 3D sets (our own code, built with the kit's set helpers): Stockholm harbour and the
// shipyard quay, the king's war camp in Poland, the lower gun deck, the explanation room at night, the sea bed in
// 1961 and the museum hall. Water is a painted plane whose texture the story scrolls (extra.water).
import * as THREE from "three";
import { NOINK } from "../ink";
import { SetBuild, lambert, basic, box, cyl, plane, glowSprite, skyCard, skyDome, makeKey } from "../kit/sets";
import { skyGrad, darkBoards, stoneWall, paving } from "../kit/paint2";
import { hullPlanks, waterTex, skylineTex, mudTex, toTex, canvas } from "./paint";
import { rng } from "../paint";

const grass = (repeat: [number, number]) => {
  const [c, g] = canvas(256, 256); const r = rng(17);
  g.fillStyle = "#7da35a"; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 300; i++) { g.fillStyle = r() < 0.5 ? "rgba(60,100,50,0.4)" : "rgba(170,200,110,0.35)"; g.fillRect(r() * 256, r() * 256, 2, 6 + r() * 6); }
  return toTex(c, repeat);
};

/** Stockholm harbour: the shipyard quay along the ship's starboard side (z < -9), sheds, a derrick, cannons waiting on
 * the quay, the town across the water (+z) and to the east, open water to the east (+x) where she sails. */
export function harbourSet(o: { cannonsOnQuay?: boolean; sheds?: boolean } = {}): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  const water = plane(root, lambert({ map: waterTex([60, 60]) }), 700, 700, 120, 0, 0, -Math.PI / 2);
  // the quay: timber-faced stone, a plank top at y 1.6
  const stone = lambert({ map: stoneWall([20, 1], 30, 46) });
  box(root, stone, 140, 2.6, 14, -10, 0.3, -16);
  box(root, lambert({ map: hullPlanks([1, 30], 21) }), 140, 0.2, 14, -10, 1.7, -16);
  for (let x = -76; x <= 56; x += 4) cyl(root, lambert({ color: "#4a3420" }), 0.25, 3.6, x, 0.6, -9.1, 8);
  // sheds and the yard
  const wall = lambert({ color: "#b98455" }), roof = lambert({ color: "#7a3b2c" });
  for (const [x, w] of (o.sheds === false ? [] : [[-44, 16], [-22, 12], [30, 14]]) as [number, number][]) {
    box(root, wall, w, 6, 8, x, 4.8, -19);
    const r = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6, 4, 4, 1), roof); r.rotation.y = Math.PI / 4; r.scale.set(w / 8.4, 1, 1.1); r.position.set(x, 9.8, -19); r.castShadow = true; root.add(r);
  }
  // the derrick that swings the guns aboard
  const timber = lambert({ color: "#5b3a22" });
  box(root, timber, 0.6, 16, 0.6, 8, 9.8, -11.5);
  const boom = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 14), timber); boom.position.set(8, 17, -5.5); boom.rotation.x = 0.35; boom.castShadow = true; root.add(boom);
  const bronze = lambert({ color: "#9a6b2c" });
  if (o.cannonsOnQuay !== false) for (let i = 0; i < 14; i++) {
    const prof2 = [[0, 0], [0.3, 0.05], [0.28, 0.4], [0.25, 2.3], [0.29, 2.42], [0.22, 2.6], [0, 2.6]].map(([r, y]) => new THREE.Vector2(r, y));
    const c = new THREE.Mesh(new THREE.LatheGeometry(prof2, 14), bronze); c.rotation.x = Math.PI / 2;
    c.position.set(-2 + (i % 7) * 0.68, 2.1 + Math.floor(i / 7) * 0.5, -13.8); c.castShadow = true; root.add(c);
  }
  // the gun on the derrick: a recognisable barrel (muzzle swell, reinforcing rings, trunnions, cascabel) in a sling
  const hanging = new THREE.Group();
  const prof = [[0, 0.3], [0.32, 0.36], [0.34, 0.3], [0.3, 0.6], [0.28, 1.6], [0.25, 2.5], [0.29, 2.62], [0.29, 2.8], [0.22, 2.85], [0, 2.85]].map(([r, y]) => new THREE.Vector2(r, y));
  const barrel = new THREE.Mesh(new THREE.LatheGeometry(prof, 18), bronze); barrel.rotation.z = Math.PI / 2; barrel.position.x = 1.4; barrel.castShadow = true; hanging.add(barrel);
  const knob = new THREE.Mesh(new THREE.SphereGeometry(0.15, 10, 8), bronze); knob.position.x = 1.4 + 0.15; hanging.add(knob);
  const trun = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.1, 0.9, 8), bronze); trun.rotation.x = Math.PI / 2; trun.position.x = 0.1; hanging.add(trun);
  for (const x of [-0.5, 0.6]) { const ring = new THREE.Mesh(new THREE.TorusGeometry(0.31, 0.05, 6, 18), lambert({ color: "#b58a3a" })); ring.rotation.y = Math.PI / 2; ring.position.x = x; hanging.add(ring); }
  hanging.visible = false; root.add(hanging);
  const line = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1, 4), lambert({ color: "#3a2a1c" })); line.visible = false; root.add(line);
  for (let i = 0; i < 6; i++) cyl(root, lambert({ color: "#7a5532" }), 0.45, 1.1, 18 + i * 1.2, 2.35, -13 - (i % 2), 10);
  // the town: across the water (+z) and closing the east; tall skyline cards on low rock
  const sky = skyDome(root, "#5f93d0", "#f0dcb4", "#f0dcb4", 1200);
  const town = new THREE.Mesh(new THREE.PlaneGeometry(260, 65), lambert({ map: skylineTex(), transparent: true, alphaTest: 0.5, side: THREE.DoubleSide }));
  town.position.set(40, 24, 150); town.rotation.y = Math.PI; root.add(town);
  const town2 = new THREE.Mesh(new THREE.PlaneGeometry(220, 55), lambert({ map: skylineTex(23), transparent: true, alphaTest: 0.5, side: THREE.DoubleSide }));
  town2.position.set(260, 20, 10); town2.rotation.y = -Math.PI / 2; root.add(town2);
  const rock = lambert({ color: "#6c6a62" });
  box(root, rock, 300, 6, 40, 40, 1, 175); box(root, rock, 40, 5, 300, 290, 1, 10);
  box(root, rock, 140, 3, 60, -10, 0.2, -50);
  // small boats
  for (const [x, z] of [[30, 40], [70, 25], [-30, 30], [95, -8]] as [number, number][]) {
    const b = new THREE.Mesh(new THREE.BoxGeometry(4, 0.8, 1.5), lambert({ color: "#6b4a2b" })); b.position.set(x, 0.3, z); b.castShadow = true; root.add(b);
  }
  const key = makeKey(root, [-60, 70, 50], [10, 0, 0], 60);
  key.shadow.camera.far = 300;
  return { root, key, glows, sky, extra: { water, hanging, line }, fogScale: 16 };
}

/** the king's camp in Poland: a striped command tent, a field table, banners, distant tents, a campfire */
export function campSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: grass([30, 30]) }), 200, 200, 0, 0, 0, -Math.PI / 2);
  const cloth = lambert({ color: "#e9dcc0" }), blue = lambert({ color: "#2a5fae" }), gold = lambert({ color: "#f2c230" });
  const tent = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 3.4, 2.6, 16, 1, true), cloth); tent.position.set(0, 1.3, -6); tent.castShadow = true; root.add(tent);
  const top = new THREE.Mesh(new THREE.ConeGeometry(3.7, 2.6, 16), blue); top.position.set(0, 3.9, -6); top.castShadow = true; root.add(top);
  const door = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 2.0), lambert({ color: "#5a4a6e" })); door.position.set(0, 1.0, -2.58); root.add(door);
  const flap = new THREE.Mesh(new THREE.PlaneGeometry(0.7, 2.1), lambert({ color: "#d8c9a8", side: THREE.DoubleSide })); flap.position.set(0.75, 1.05, -2.5); flap.rotation.y = -0.6; root.add(flap);
  // the war: field guns, a palisade, powder smoke drifting over the camp
  const iron = lambert({ color: "#3a3a46" }), wheel = lambert({ color: "#5b3a22" });
  for (const [x, z] of [[-9, -12], [7, -14], [12, -10]] as [number, number][]) {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.24, 2.4, 12), iron); b.rotation.z = Math.PI / 2 - 0.15; b.position.set(x, 0.75, z); b.castShadow = true; root.add(b);
    for (const dz of [-0.4, 0.4]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.1, 14), wheel); w.rotation.x = Math.PI / 2; w.position.set(x + 0.5, 0.45, z + dz); root.add(w); }
  }
  for (let x = -30; x <= 30; x += 1.2) { const p = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 2.2, 6), wheel); p.position.set(x, 1.1, -34 + Math.sin(x) * 0.4); root.add(p); }
  cyl(root, lambert({ color: "#5b3a22" }), 0.05, 2, 0, 6.2, -6);
  const banner = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.0), blue); banner.position.set(0.8, 6.8, -6); root.add(banner);
  const cross = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 0.2), gold); cross.position.set(0.8, 6.8, -5.99); root.add(cross);
  // field table and stool in front of the tent
  const wood = lambert({ color: "#6b4a2b" });
  box(root, wood, 1.6, 0.08, 0.9, 0.6, 0.78, -1.4);
  for (const [x, z] of [[-0.1, -1.75], [1.3, -1.75], [-0.1, -1.05], [1.3, -1.05]]) box(root, wood, 0.07, 0.78, 0.07, x, 0.39, z);
  box(root, lambert({ color: "#f4eee1" }), 0.5, 0.02, 0.35, 0.4, 0.83, -1.4);
  cyl(root, lambert({ color: "#2a2034" }), 0.05, 0.12, 0.95, 0.88, -1.5, 10);
  // the camp beyond: tents, banners, a fire
  for (let i = 0; i < 9; i++) {
    const x = -24 + i * 6 + (i % 2) * 2, z = -22 - (i % 3) * 5;
    const t = new THREE.Mesh(new THREE.ConeGeometry(2, 2.6, 8), cloth); t.position.set(x, 1.3, z); t.castShadow = true; root.add(t);
  }
  box(root, lambert({ color: "#3a2a1c" }), 1.2, 0.2, 1.2, -5, 0.1, -9);
  glows.push(glowSprite(root, [255, 170, 90], 3, -5, 0.8, -9));
  const sky = skyDome(root, "#5d82c0", "#e8d2ac", "#e8d2ac", 400);
  const key = makeKey(root, [12, 18, 10], [0, 0, -4], 14);
  return { root, key, glows, sky, extra: {}, fogScale: 3 };
}

/** the lower gun deck: a long low room, beams, a row of bronze guns on red carriages each side, the open ports
 * (bright squares of sky and sea). extra.flood = the water sheet the story raises; extra.room = the part that heels. */
export function gundeckSet(): SetBuild {
  const root = new THREE.Group();
  const room = new THREE.Group(); root.add(room);
  const glows: THREE.Object3D[] = [];
  const planks = lambert({ map: darkBoards([2, 10]) });
  plane(room, planks, 9.6, 40, 0, 0, 0, -Math.PI / 2);
  const ceil = plane(room, lambert({ map: darkBoards([2, 10], 9) }), 9.6, 40, 0, 2.0, 0, Math.PI / 2); void ceil;
  for (let z = -18; z <= 18; z += 1.6) box(room, lambert({ color: "#3e2a1a" }), 9.6, 0.22, 0.26, 0, 1.88, z);
  const wallMat = lambert({ map: hullPlanks([4, 1], 9), side: THREE.DoubleSide });
  const outside = basic({ map: skyGrad("#8fb8e0", "#cfe2ee", "#3f8fa6") });
  const red = lambert({ color: "#b8352a" }), bronze = lambert({ color: "#9a6b2c" }), wood = lambert({ color: "#5b3a22" });
  for (const side of [1, -1]) {
    plane(room, wallMat, 40, 2.0, side * 4.8, 1.0, 0, 0, -side * Math.PI / 2);
    for (let k = 0; k < 11; k++) {
      const z = -16 + k * 3.2;
      const hole = new THREE.Mesh(new THREE.PlaneGeometry(0.8, 0.8), outside); hole.position.set(side * 4.78, 0.95, z); hole.rotation.y = -side * Math.PI / 2; hole.layers.set(NOINK); room.add(hole);
      glows.push(glowSprite(room, [255, 236, 200], 1.6, side * 4.4, 0.95, z));
      const car = new THREE.Mesh(new THREE.BoxGeometry(1.6, 0.45, 0.7), red); car.position.set(side * 3.5, 0.32, z); car.castShadow = true; room.add(car);
      for (const dz of [-0.36, 0.36]) for (const dx of [-0.6, 0.6]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.1, 12), wood); w.rotation.x = Math.PI / 2; w.position.set(side * 3.5 + dx, 0.17, z + dz); room.add(w); }
      const gun = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.25, 2.6, 12), bronze); gun.rotation.z = Math.PI / 2; gun.position.set(side * 3.8, 0.72, z); gun.castShadow = true; room.add(gun);
    }
  }
  const flood = new THREE.Mesh(new THREE.PlaneGeometry(9.6, 40), new THREE.MeshLambertMaterial({ map: waterTex([3, 12], 7), transparent: true, opacity: 0.88 }));
  flood.rotation.x = -Math.PI / 2; flood.position.y = -0.2; root.add(flood);
  for (let z = -16; z <= 16; z += 8) glows.push(glowSprite(room, [255, 214, 160], 4, 0, 1.6, z));
  const key = makeKey(root, [12, 6, 4], [0, 0, 0], 22);
  return { root, key, glows, extra: { flood, room } };
}

/** the explanation room at night: dark boards, stone walls, one tall moonlit window, a long bench */
export function explainSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: darkBoards([4, 4]) }), 30, 30, 0, 0, -4, -Math.PI / 2);
  const stone = lambert({ map: stoneWall([4, 2], 228, 40) });
  box(root, stone, 24, 9, 0.3, 0, 4.5, -12);
  box(root, stone, 0.3, 9, 20, -12, 4.5, -2);
  box(root, stone, 0.3, 9, 20, 12, 4.5, -2);
  const win = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 4.6), basic({ map: skyGrad("#08112e", "#16245a", "#2a3a7a", 160) }));
  win.position.set(-6, 4, -11.8); win.layers.set(NOINK); root.add(win);
  glows.push(glowSprite(root, [140, 160, 255], 5, -6, 4.4, -11.4));
  glows.push(glowSprite(root, [255, 190, 110], 4, 4, 2.4, -6));
  const key = makeKey(root, [-10, 14, 4], [0, 0, -4], 12);
  return { root, key, glows, extra: {} };
}

/** the sea bed in 1961: mud, a green underwater fog (the preset), the surface far above, light shafts */
export function seabedSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: mudTex([30, 30]) }), 400, 400, 0, -32, 0, -Math.PI / 2);
  const surf = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), basic({ color: "#7fc0c4", side: THREE.DoubleSide, transparent: true, opacity: 0.6 }));
  surf.rotation.x = Math.PI / 2; surf.position.y = 0; surf.layers.set(NOINK); root.add(surf);
  for (let i = 0; i < 0; i++) {   // light shafts read as dark bars under the ink pass: off
    const s = new THREE.Mesh(new THREE.PlaneGeometry(4, 60), basic({ color: "#cfe9e0", transparent: true, opacity: 0.12, depthWrite: false, side: THREE.DoubleSide }));
    s.position.set(-40 + i * 16, -16, -30 - (i % 3) * 8); s.rotation.z = 0.25; s.layers.set(NOINK); root.add(s);
  }
  // the salvage pontoons on the surface and their cables
  for (const x of [-12, 12]) {
    const p = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, 30, 16), lambert({ color: "#3a3f4a" })); p.rotation.x = Math.PI / 2; p.position.set(x, 0.5, 0); root.add(p);
  }
  const key = makeKey(root, [10, 60, 20], [0, -30, 0], 50);
  return { root, key, glows, extra: { surf }, fogScale: 1.8 };
}

/** the museum hall: a tall dark hall, a stone floor, warm pools of light, the ship on a cradle (the story's rig) */
export function museumHallSet(): SetBuild {
  const root = new THREE.Group();
  const glows: THREE.Object3D[] = [];
  plane(root, lambert({ map: paving([20, 20], 220, 30, 4) }), 140, 140, 0, -5.2, 0, -Math.PI / 2);
  const wall = lambert({ color: "#2a2d3e" });
  box(root, wall, 140, 70, 1, 0, 30, -40); box(root, wall, 1, 70, 140, -60, 30, 0); box(root, wall, 1, 70, 140, 60, 30, 0);
  const cradle = lambert({ color: "#5c5f6e" });
  for (const x of [-16, -6, 4, 14]) box(root, cradle, 1.2, 2.2, 8, x, -4.1, 0);
  box(root, lambert({ color: "#23263a" }), 140, 1, 140, 0, 64, 0);
  for (let x = -54; x <= 54; x += 12) box(root, lambert({ color: "#33364a" }), 1.2, 1.6, 140, x, 63, 0);
  // a gallery walkway with a rail at deck height along the far wall
  box(root, lambert({ color: "#3d4052" }), 120, 0.5, 6, 0, 6, -30);
  for (let x = -58; x <= 58; x += 2) box(root, lambert({ color: "#8a8fa6" }), 0.1, 1.1, 0.1, x, 6.8, -27.2);
  box(root, lambert({ color: "#8a8fa6" }), 120, 0.12, 0.12, 0, 7.4, -27.2);
  // spotlights: soft cones from the ceiling onto the hull, and their pools
  for (const [x, z] of [[-18, 9], [0, 10], [18, 9], [-10, -9], [10, -9]] as [number, number][]) {
    const cone = new THREE.Mesh(new THREE.ConeGeometry(7, 60, 24, 1, true), basic({ color: "#ffe3b8", transparent: true, opacity: 0.07, depthWrite: false, side: THREE.DoubleSide, blending: THREE.AdditiveBlending }));
    cone.position.set(x, 33, z); cone.layers.set(NOINK); root.add(cone);
    glows.push(glowSprite(root, [255, 210, 150], 16, x, 2, z * 0.6));
  }
  const key = makeKey(root, [20, 50, 30], [0, 0, 0], 50);
  return { root, key, glows, extra: {}, fogScale: 2.5 };
}
