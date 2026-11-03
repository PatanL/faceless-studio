// Key frame + depth 2.5D plate (our own code; round 3 pilot, technique 1). A camera-space grid mesh displaced by a
// monocular depth estimate of a key frame (scratch d25/plate.py writes it), textured with the key frame from the key
// camera, so seen from that camera it is the key frame exactly; small camera moves give real parallax. Measured limits
// (hook key frame): stretch stays under ~3 % of the frame for a 0.1 m push, 1 deg orbit or 5 cm truck; tilts are
// limited by the plate's edge (1 deg leaves 2.4 % uncovered); zoom is free of stretch but costs resolution.
//   depthPlate(id, keyCam)  a Rig: the plate public/kf/<id>_plate.json + public/kf/<id>_kf.png placed at the key camera
import * as THREE from "three";
import { staticFile } from "remotion";
import { NOINK } from "../ink";
import type { Rig } from "./Stage";
import type { CamKey } from "./campath";

const plates = new Map<string, { geo: THREE.BufferGeometry; tex: THREE.Texture }>();
const dec = (b64: string, T: typeof Float32Array | typeof Uint32Array) => { const s = atob(b64), u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new T(u.buffer); };
export async function preloadPlate(id: string) {
  if (plates.has(id)) return;
  const j = await (await fetch(staticFile(`kf/${id}_plate.json`))).json();
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(dec(j.position, Float32Array) as Float32Array, 3));
  geo.setAttribute("uv", new THREE.BufferAttribute(dec(j.uv, Float32Array) as Float32Array, 2));
  geo.setIndex(new THREE.BufferAttribute(dec(j.index, Uint32Array) as Uint32Array, 1));
  const tex = await new THREE.TextureLoader().loadAsync(staticFile(`kf/${id}_kf.png`)); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8;
  plates.set(id, { geo, tex });
}
/** the plate as a rig, placed so its camera space is the key camera's (keyCam: the CamKey the key frame was framed for) */
export const depthPlate = (id: string, keyCam: CamKey): Rig => (ctx) => {
  const p = plates.get(id); const g = new THREE.Group();
  if (!p) { console.warn(`[plate] ${id} not preloaded`); return () => {}; }
  // the key frame is already lit, inked and graded: an unlit, untoned, unfogged surface, outside the ink pass
  const m = new THREE.Mesh(p.geo, new THREE.MeshBasicMaterial({ map: p.tex, fog: false, toneMapped: false, side: THREE.DoubleSide }));
  m.layers.set(NOINK); g.add(m);
  const cam = new THREE.PerspectiveCamera(); cam.position.set(...keyCam.pos); cam.lookAt(new THREE.Vector3(...keyCam.look)); cam.updateMatrixWorld();
  g.position.copy(cam.position); g.quaternion.copy(cam.quaternion); ctx.root.add(g);
  return () => {};
};
