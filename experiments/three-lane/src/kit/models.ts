// The kit's CC0 model library (our own code; geometry from Poly Haven, see public/models/ph/LICENSES.md).
// Every model is restyled to our look: its stock textures were never downloaded; each material is replaced by a
// two-tone Lambert with a code-painted texture or a palette colour chosen by the model's kind and the material's name
// (wood grain, stone, terracotta, wicker, bronze, iron, leaf, bark), the world ink pass outlines it, and placed models
// get a soft contact shadow. Usage:
//   await preloadModels()              (Episode3D does this before any Stage mounts)
//   model("barrel_03", { scale, tint }) -> a THREE.Group clone, feet on y = 0, castShadow / receiveShadow set
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { staticFile } from "remotion";
import { lambert } from "./sets";
import { grainPlanks, stoneCourses } from "./dressing";
import { brass } from "./paint2";
import { rng } from "../paint";
import { NOINK } from "../ink";

export type Kind = "wood" | "wicker" | "clay" | "bronze" | "rock" | "bark" | "leaf" | "tool";
export const LIBRARY: Record<string, Kind> = {
  barrel_03: "wood", wine_barrel_01: "wood", wooden_barrels_01: "wood", wooden_crate_01: "wood", wooden_crate_02: "wood",
  wooden_bucket_01: "wood", wicker_basket_01: "wicker", wicker_basket_02: "wicker", ceramic_pot: "clay", ceramic_vase_01: "clay",
  ceramic_vase_03: "clay", planter_pot_clay: "clay", brass_pot_01: "bronze", wooden_bowl_02: "wood", rock_07: "rock", rock_09: "rock",
  moon_rock_02: "rock", moon_rock_04: "rock", namaqualand_boulders_01: "rock", tree_stump_01: "bark", fern_02: "leaf", nettle_plant: "leaf",
  wooden_axe: "tool", cross_pein_hammer: "tool", sledgehammer_01: "tool", rusted_spade_01: "tool", wooden_ladder: "wood",
  wooden_lantern_01: "wood", stone_fire_pit: "rock", kite_shield: "tool", wooden_broom: "wood", wooden_stool_01: "wood",
  painted_wooden_table: "wood", painted_wooden_bench: "wood", wooden_display_shelves_01: "wood", wooden_picnic_table: "wood",
  dutch_ship_medium: "wood", modular_wooden_pier: "wood",
};
export type ModelId = keyof typeof LIBRARY;

const cache = new Map<string, THREE.Group>();
let loading: Promise<void> | null = null;
/** load every library model once (geometry only, a few MB in all) */
export function preloadModels(ids: string[] = Object.keys(LIBRARY)): Promise<void> {
  if (loading) return loading;
  const loader = new GLTFLoader();
  loading = Promise.all(ids.map(async (id) => {
    try {
      const g = await loader.loadAsync(staticFile(`models/ph/${id}/${id}.gltf`));
      cache.set(id, g.scene);
    } catch (e) { console.warn(`[models] ${id} failed to load`, e); }
  })).then(() => undefined);
  return loading;
}
export const modelsReady = () => cache.size > 0;

// ---- painted materials by kind (shared per kind + seed, so a scene of 40 barrels is a handful of materials)
const canvas = (w: number, h: number) => { const c = document.createElement("canvas"); c.width = w; c.height = h; return [c, c.getContext("2d")!] as const; };
const tex = (c: HTMLCanvasElement) => { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; return t; };
function mottle(base: string, spots: string[], seed: number, n = 120, lines?: string) {
  const [c, g] = canvas(256, 256), r = rng(seed);
  g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  for (let k = 0; k < n; k++) { g.fillStyle = spots[k % spots.length]; g.globalAlpha = 0.25 + r() * 0.35; g.beginPath(); g.ellipse(r() * 256, r() * 256, 4 + r() * 22, 3 + r() * 12, r() * 3, 0, 7); g.fill(); }
  g.globalAlpha = 1;
  if (lines) { g.strokeStyle = lines; g.lineWidth = 2; for (let k = 0; k < 14; k++) { const x = r() * 256, y = r() * 256; g.beginPath(); g.moveTo(x, y); g.lineTo(x + (r() - 0.5) * 70, y + (r() - 0.5) * 70); g.stroke(); } }
  // a soft top-lit gradient so no surface is one flat value
  const grd = g.createLinearGradient(0, 0, 0, 256); grd.addColorStop(0, "rgba(255,240,210,0.14)"); grd.addColorStop(1, "rgba(30,20,60,0.14)");
  g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
  return tex(c);
}
function woven(base: string, dark: string) {
  const [c, g] = canvas(128, 128);
  g.fillStyle = base; g.fillRect(0, 0, 128, 128);
  for (let y = 0; y < 128; y += 16) for (let x = 0; x < 128; x += 16) {
    g.fillStyle = (x + y) % 32 ? dark : base; g.fillRect(x + 1, y + 1, 14, 14);
    g.strokeStyle = "rgba(40,25,10,0.5)"; g.lineWidth = 2; g.strokeRect(x + 1, y + 1, 14, 14);
  }
  return tex(c);
}
const mats = new Map<string, THREE.Material>();
function matFor(kind: Kind, name: string, seed: number, tint?: string): THREE.Material {
  const n = name.toLowerCase();
  // the material's own name overrides the model kind (an axe has a wooden handle and an iron head)
  const k: Kind | "iron" = /metal|iron|steel|blade|head|band|hoop|nail|rim|ring/.test(n) && kind !== "bronze" ? "iron"
    : /wood|handle|plank|stick|shaft/.test(n) ? "wood" : /rope|wicker/.test(n) ? "wicker" : /leaf|leaves|frond/.test(n) ? "leaf" : kind;
  const key = `${k}:${seed % 4}:${tint ?? ""}`;
  if (mats.has(key)) return mats.get(key)!;
  let m: THREE.Material;
  switch (k) {
    case "wood": case "tool": m = lambert({ map: grainPlanks([1, 1], { hue: 24 + (seed % 4) * 4, light: 38 + (seed % 3) * 5, boards: 3, seed: 30 + seed }) }); break;
    case "iron": m = lambert({ color: "#4a4658" }); break;
    case "bronze": m = lambert({ map: brass() }); break;
    case "clay": m = lambert({ map: mottle(["#c8693a", "#b85a32", "#d07a48", "#c27040"][seed % 4], ["#e29a68", "#8e4426", "#f0c090"], 50 + seed) }); break;
    case "wicker": m = lambert({ map: woven("#c9a46a", "#a8834e") }); break;
    case "rock": m = lambert({ map: (seed % 2 ? mottle("#a49a8e", ["#7c7268", "#c4bbae", "#8a8478"], 70 + seed, 140, "rgba(60,50,60,0.4)") : stoneCourses([1, 1], { hue: 32, light: 56, seed: 70 + seed, moss: false })) }); break;
    case "bark": m = lambert({ map: mottle("#6b4a30", ["#4a3020", "#8a6440"], 90 + seed, 90, "rgba(40,25,15,0.6)") }); break;
    case "leaf": m = lambert({ color: ["#5f8f4a", "#6f9a4e", "#4f7f40"][seed % 3], side: THREE.DoubleSide }); break;
  }
  if (tint) (m as THREE.MeshLambertMaterial).color.multiply(new THREE.Color(tint));
  mats.set(key, m!);
  return m!;
}

let blobTex: THREE.Texture | null = null;
function contactBlob(w: number, d: number) {
  if (!blobTex) {
    const [c, g] = canvas(128, 128);
    const grd = g.createRadialGradient(64, 64, 6, 64, 64, 62);
    grd.addColorStop(0, "rgba(40,30,70,0.55)"); grd.addColorStop(0.6, "rgba(40,30,70,0.25)"); grd.addColorStop(1, "rgba(40,30,70,0)");
    g.fillStyle = grd; g.fillRect(0, 0, 128, 128);
    blobTex = new THREE.CanvasTexture(c);
  }
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, d), new THREE.MeshBasicMaterial({ map: blobTex, transparent: true, depthWrite: false, fog: false, toneMapped: false }));
  m.rotation.x = -Math.PI / 2; m.position.y = 0.006; m.layers.set(NOINK); m.renderOrder = 1;
  return m;
}

/** a restyled clone of a library model: feet on y = 0, centred on x/z; with a soft contact shadow under it */
export function model(id: string, o: { scale?: number; tint?: string; seed?: number; contact?: boolean } = {}): THREE.Group {
  const src = cache.get(id);
  const out = new THREE.Group();
  if (!src) { console.warn(`[models] ${id} not preloaded`); return out; }
  const g = src.clone(true);
  const kind = (LIBRARY[id] ?? "wood") as Kind, seed = o.seed ?? 0;
  g.traverse((ob: THREE.Object3D) => {
    const m = ob as THREE.Mesh;
    if (!m.isMesh) return;
    const name = (Array.isArray(m.material) ? m.material[0] : m.material)?.name ?? m.name;
    m.material = matFor(kind, `${name} ${m.name}`, seed, o.tint);
    m.castShadow = true; m.receiveShadow = true;
  });
  g.scale.setScalar(o.scale ?? 1);
  const bb = new THREE.Box3().setFromObject(g);
  g.position.set(-(bb.min.x + bb.max.x) / 2, -bb.min.y, -(bb.min.z + bb.max.z) / 2);
  out.add(g);
  if (o.contact !== false) { const sz = bb.getSize(new THREE.Vector3()); out.add(contactBlob(sz.x * 1.35, sz.z * 1.35)); }
  out.userData.size = bb.getSize(new THREE.Vector3());
  return out;
}
