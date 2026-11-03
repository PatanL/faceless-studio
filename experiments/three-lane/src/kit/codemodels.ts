// Code-generated models (our own code; owner, round 3: "everything must be done in code"). Meshes our own scripts
// sculpt (scripts/sdf_dragon.py: signed distance fields, smooth unions, marching cubes) and ship as compact JSON under
// public/models/code/. Episode3D preloads them with preloadCodeModels(); builders add the small parts (teeth, eyes,
// whiskers, the ball) at the anchors the generator exported.
//   sdfDragon(o)   the code-sculpted Chinese dragon head (gold with scale normals, ink outlined), mouth open, +z forward
import * as THREE from "three";
import { staticFile } from "remotion";
import { metal, glaze } from "./materials";
import { taperTube } from "./heroprops";
import type { V3 } from "./Stage";

type Mesh = { geo: THREE.BufferGeometry; anchors: Record<string, V3 | V3[]> };
const cache = new Map<string, Mesh>();
let loading: Promise<void> | null = null;
const dec = (b64: string, T: typeof Float32Array | typeof Uint32Array) => { const s = atob(b64), u = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) u[i] = s.charCodeAt(i); return new T(u.buffer); };

export function preloadCodeModels(ids: string[] = ["dragon_sdf"]): Promise<void> {
  if (loading) return loading;
  loading = Promise.all(ids.map(async (id) => {
    try {
      const j = await (await fetch(staticFile(`models/code/${id}.json`))).json();
      const geo = new THREE.BufferGeometry();
      geo.setAttribute("position", new THREE.BufferAttribute(dec(j.position, Float32Array) as Float32Array, 3));
      geo.setAttribute("normal", new THREE.BufferAttribute(dec(j.normal, Float32Array) as Float32Array, 3));
      geo.setAttribute("uv", new THREE.BufferAttribute(dec(j.uv, Float32Array) as Float32Array, 2));
      geo.setIndex(new THREE.BufferAttribute(dec(j.index, Uint32Array) as Uint32Array, 1));
      geo.computeBoundingSphere();
      cache.set(id, { geo, anchors: j.anchors });
    } catch (e) { console.warn(`[codemodels] ${id} failed to load`, e); }
  })).then(() => undefined);
  return loading;
}

/** the code-sculpted dragon head: gold (scale normals) body, ivory teeth, amber eyes, curling whiskers, red mouth */
export function sdfDragon(o: { mat?: THREE.Material; whiskers?: boolean } = {}): THREE.Group {
  const g = new THREE.Group(), m = cache.get("dragon_sdf");
  if (!m) { console.warn("[codemodels] dragon_sdf not preloaded"); return g; }
  const gold = o.mat ?? metal("gold", { scales: 14, repeat: [1, 1] });
  const bodyMat = (gold as THREE.MeshStandardMaterial).clone(); bodyMat.side = THREE.DoubleSide; bodyMat.userData.env = true;
  const body = new THREE.Mesh(m.geo, bodyMat); body.castShadow = true; body.receiveShadow = true; g.add(body);
  const A = m.anchors as Record<string, V3[] & V3>;
  const tooth = glaze("#f4ead2", { rough: 0.25 }), fine = metal("gold", { grain: true });
  (A.upperTeeth as unknown as V3[]).forEach((p, i) => { const t = new THREE.Mesh(new THREE.ConeGeometry(0.022, i % 7 === 0 ? 0.16 : 0.07, 7), tooth); t.position.set(p[0], p[1] - 0.03, p[2]); t.rotation.x = Math.PI; g.add(t); });
  (A.lowerTeeth as unknown as V3[]).forEach((p, i) => { const t = new THREE.Mesh(new THREE.ConeGeometry(0.02, i % 7 === 1 ? 0.15 : 0.06, 7), tooth); t.position.set(p[0], p[1] + 0.03, p[2]); g.add(t); });
  const mouth = new THREE.Mesh(new THREE.SphereGeometry(0.1, 16, 12), new THREE.MeshStandardMaterial({ color: "#7a1a14", roughness: 0.6 })); mouth.scale.set(1.0, 0.9, 3.0); mouth.position.set(...(A.mouth as V3)); mouth.position.z -= 0.08; g.add(mouth);
  for (const e of A.eyes as unknown as V3[]) {
    const eye = new THREE.Mesh(new THREE.SphereGeometry(0.06, 18, 14), glaze("#e8b84a", { rough: 0.12 })); eye.position.set(...e); g.add(eye);
    const pup = new THREE.Mesh(new THREE.SphereGeometry(0.03, 12, 10), glaze("#140c08", { rough: 0.1 })); pup.scale.set(0.45, 1.1, 0.6); pup.position.set(e[0] * 1.08, e[1], e[2] + 0.052); g.add(pup);
  }
  if (o.whiskers !== false) for (const r of A.whiskerRoots as unknown as V3[]) {
    const s = Math.sign(r[0]), P = (x: number, y: number, z: number) => new THREE.Vector3(r[0] + s * x, r[1] + y, r[2] + z);
    g.add(taperTube(new THREE.CatmullRomCurve3([P(0, 0, 0), P(0.12, 0.08, 0.06), P(0.24, 0.24, -0.02), P(0.3, 0.42, -0.24), P(0.26, 0.5, -0.5), P(0.3, 0.44, -0.78)]), (u) => 0.022 * (1 - u) + 0.004, 48, 6, fine));
  }
  return g;
}
