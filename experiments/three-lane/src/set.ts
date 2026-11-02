// The test set (our own code): a palace-hall corner. Two plaster walls with a red lacquer wainscot and top beam,
// a lattice window in the left wall with sky behind it, a lacquer pillar, a plank floor with a rug, and three
// Poly Haven CC0 props (cabinet, tea table, armchair) re-shaded two-tone. One warm key light casts the shadows.
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { staticFile } from "remotion";
import { twoTone, TONE } from "./shade";
import { NOINK } from "./ink";
import { woodFloor, plaster, lacquer, rug, sky } from "./paint";
import { makeCard, Card } from "./card";

export const HORIZON = "#efcfa2"; // warm horizon: fog, background, bottom of the sky
const SKY_TOP = "#8fb0d6";

const MODELS = {
  cabinet: "models/chinese_cabinet/chinese_cabinet_1k.gltf",
  table: "models/chinese_tea_table/chinese_tea_table_1k.gltf",
  chair: "models/chinese_armchair/chinese_armchair_1k.gltf",
} as const;
export type Kit = Record<keyof typeof MODELS, THREE.Object3D>;

export async function loadKit(): Promise<Kit> {
  const loader = new GLTFLoader();
  const entries = await Promise.all(Object.entries(MODELS).map(async ([k, url]) => {
    const gltf = await loader.loadAsync(staticFile(url));
    return [k, gltf.scene] as const;
  }));
  return Object.fromEntries(entries) as Kit;
}

const lambert = (p: THREE.MeshLambertMaterialParameters) => twoTone(new THREE.MeshLambertMaterial(p));

/** PBR glTF materials -> two-tone Lambert with the same albedo map; stand the prop on the floor at (x, z). */
function place(src: THREE.Object3D, x: number, z: number, rotY: number) {
  const o = src.clone(true);
  o.traverse((n) => {
    const m = n as THREE.Mesh;
    if (!m.isMesh) return;
    const old = m.material as THREE.MeshStandardMaterial;
    m.material = lambert({ map: old.map, color: old.color, side: old.side });
    m.castShadow = true; m.receiveShadow = true;
  });
  o.rotation.y = rotY;
  o.updateMatrixWorld(true);
  const box = new THREE.Box3().setFromObject(o);
  const c = box.getCenter(new THREE.Vector3());
  o.position.set(x - c.x, -box.min.y, z - c.z);
  return o;
}

export type SetBuild = { root: THREE.Group; card: Card; fog: THREE.Fog; key: THREE.DirectionalLight; focus: THREE.Vector3 };

export function buildSet(kit: Kit): SetBuild {
  const root = new THREE.Group();
  const add = (geo: THREE.BufferGeometry, mat: THREE.Material, x: number, y: number, z: number) => {
    const m = new THREE.Mesh(geo, mat);
    m.position.set(x, y, z); m.castShadow = true; m.receiveShadow = true;
    root.add(m); return m;
  };

  // corner at (-2.5, -2.5); room interior is x, z > -2.5; walls 4.6 m tall
  const H = 4.6, X0 = -2.5, Z0 = -2.5, L = 9;
  const floorMat = lambert({ map: woodFloor([3, 3]) });
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(L, L), floorMat);
  floor.rotation.x = -Math.PI / 2; floor.position.set(X0 + L / 2, 0, Z0 + L / 2); floor.receiveShadow = true;
  root.add(floor);

  const wallMat = lambert({ map: plaster([2, 1]) });
  const lac = lambert({ map: lacquer() });
  add(new THREE.BoxGeometry(L, H, 0.2), wallMat, X0 + L / 2, H / 2, Z0 - 0.1); // back wall
  // left wall with a window opening: z in [-0.9, 0.5], y in [1.0, 3.0]
  const wz0 = -0.9, wz1 = 0.5, wy0 = 1.0, wy1 = 3.0, wx = X0 - 0.1;
  add(new THREE.BoxGeometry(0.2, wy0, L), wallMat, wx, wy0 / 2, Z0 + L / 2);
  add(new THREE.BoxGeometry(0.2, H - wy1, L), wallMat, wx, (H + wy1) / 2, Z0 + L / 2);
  add(new THREE.BoxGeometry(0.2, wy1 - wy0, wz0 - Z0), wallMat, wx, (wy0 + wy1) / 2, (Z0 + wz0) / 2);
  add(new THREE.BoxGeometry(0.2, wy1 - wy0, Z0 + L - wz1), wallMat, wx, (wy0 + wy1) / 2, (wz1 + Z0 + L) / 2);
  // window frame + lattice (lacquer)
  const fw = 0.12, fz = (wz0 + wz1) / 2, fwid = wz1 - wz0, fh = wy1 - wy0;
  add(new THREE.BoxGeometry(0.26, fw, fwid + 2 * fw), lac, X0 + 0.02, wy0 - fw / 2, fz);
  add(new THREE.BoxGeometry(0.26, fw, fwid + 2 * fw), lac, X0 + 0.02, wy1 + fw / 2, fz);
  add(new THREE.BoxGeometry(0.26, fh, fw), lac, X0 + 0.02, (wy0 + wy1) / 2, wz0 - fw / 2);
  add(new THREE.BoxGeometry(0.26, fh, fw), lac, X0 + 0.02, (wy0 + wy1) / 2, wz1 + fw / 2);
  for (let i = 1; i < 4; i++) add(new THREE.BoxGeometry(0.05, fh, 0.035), lac, X0 - 0.02, (wy0 + wy1) / 2, wz0 + (fwid * i) / 4);
  for (let i = 1; i < 5; i++) add(new THREE.BoxGeometry(0.05, 0.035, fwid), lac, X0 - 0.02, wy0 + (fh * i) / 5, fz);
  // sky card outside the window (no ink, no fog, unlit)
  const skyMat = new THREE.MeshBasicMaterial({ map: sky(SKY_TOP, HORIZON), fog: false });
  const skyPlane = new THREE.Mesh(new THREE.PlaneGeometry(14, 8), skyMat);
  skyPlane.rotation.y = Math.PI / 2; skyPlane.position.set(X0 - 3, 2.4, fz); skyPlane.layers.set(NOINK);
  root.add(skyPlane);

  // wainscot + top beam on both walls, lacquer pillar with a stone base
  add(new THREE.BoxGeometry(L, 0.85, 0.06), lac, X0 + L / 2, 0.425, Z0 + 0.03);
  add(new THREE.BoxGeometry(0.06, 0.85, L), lac, X0 + 0.03, 0.425, Z0 + L / 2);
  add(new THREE.BoxGeometry(L, 0.32, 0.22), lac, X0 + L / 2, H - 0.16, Z0 + 0.11);
  add(new THREE.BoxGeometry(0.22, 0.32, L), lac, X0 + 0.11, H - 0.16, Z0 + L / 2);
  add(new THREE.CylinderGeometry(0.2, 0.2, H, 24), lac, 1.7, H / 2, -1.7);
  add(new THREE.CylinderGeometry(0.3, 0.34, 0.22, 24), lambert({ color: "#b9ad9a" }), 1.7, 0.11, -1.7);

  const rugMesh = add(new THREE.BoxGeometry(2.6, 0.02, 1.9), lambert({ map: rug() }), -0.6, 0.01, 0.5);
  rugMesh.castShadow = false;

  // props (Poly Haven CC0)
  root.add(place(kit.cabinet, -0.6, Z0 + 0.32, 0));
  root.add(place(kit.table, -0.5, 0.45, 0.2));
  root.add(place(kit.chair, -1.65, 0.85, 1.0));

  // key light (warm, from front-right, high) = the only shadow caster; twoTone takes its colours from TONE
  const key = new THREE.DirectionalLight("#ffe2b8", 2.0);
  key.position.set(4.5, 7.5, 6.0); key.target.position.set(-0.5, 0, -0.5);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6, near: 1, far: 25 });
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.02;
  root.add(key, key.target);
  TONE.uLitCol.value.set(1.42, 1.28, 1.06);   // warm key
  TONE.uShadeCol.value.set(0.50, 0.49, 0.80); // violet-blue shade

  const card = makeCard(new THREE.Vector3(0.55, 0, 1.05), new THREE.Vector3(1.06, 0.98, 0.88), new THREE.Vector3(0.62, 0.62, 0.88));
  root.add(card.group);

  const fog = new THREE.Fog(HORIZON, 4.5, 26);
  return { root, card, fog, key, focus: new THREE.Vector3(0.55, 1.05, 1.05) };
}
