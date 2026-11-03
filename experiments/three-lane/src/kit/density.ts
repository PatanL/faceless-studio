// Scene density presets (our own code; coordinator round 2: "sparse coded primitives, one small figure per shot").
// Fill the midground and background up to the references' detail (frames30 tiles: edge density median 0.092, flat
// share 0.40; Barca v14 and Vasa sat at ~0.07 / ~0.5). Deterministic, keep-out boxes for actors and camera paths.
//   fill(root, preset, area, o)   scatter a preset's models and architecture over [x0, z0, x1, z1]
//     presets: "camp" (tents, standards, fire pits, carts, stores), "market" (stalls, baskets, pots, carts), "street"
//     (barrels, crates, amphorae, baskets against walls), "wallfoot" (stones, baskets, timber, ladders, tools),
//     "workshop" (anvil-like stumps, tools, buckets, shelves), "shore" (rocks, boats' gear, barrels, pier bits)
//   crowd(area, n, o)   PersonSpec[] for a readable crowd: Actors in staggered rows, mixed costumes and faces,
//     facing a point; front rows big enough to read as people (use with castKey "medium" / "wide")
import * as THREE from "three";
import type { PersonSpec, V3 } from "./Stage";
import type { Box } from "./framing";
import { model } from "./models";
import { tent, cart, stall, standard, well, palm } from "./architecture";
import { rng } from "../paint";

type Item = { make: (seed: number) => THREE.Object3D; r: number; w: number };
const M = (id: string, s = 1, r = 0.4): Item => ({ make: (seed) => model(id, { scale: s * (0.85 + (seed % 5) * 0.07), seed }), r, w: 1 });
const PRESETS: Record<string, Item[]> = {
  camp: [{ make: (s) => tent({ seed: s, a: ["#e9dcc0", "#d8c49c", "#c94b3a", "#e0b04a"][s % 4], b: ["#d8c49c", "#efe3c8", "#e9dcc0", "#c9a46a"][s % 4] }), r: 4.2, w: 3 },
    { make: (s) => standard(["#c94b3a", "#7a2a4a", "#e0b04a", "#2f5aa8"][s % 4], 5 + (s % 3)), r: 0.8, w: 1 },
    { make: () => model("stone_fire_pit"), r: 1.2, w: 1 }, { make: (s) => cart({ seed: s }), r: 2.2, w: 1 },
    M("wooden_crate_01"), M("barrel_03"), M("wicker_basket_01"), M("wooden_barrels_01", 0.8, 0.9)],
  market: [{ make: (s) => stall({ seed: s, a: ["#c94b3a", "#2f5aa8", "#3f8a5a", "#e0b04a"][s % 4] }), r: 2.0, w: 3 },
    M("wicker_basket_02"), M("ceramic_vase_01"), M("ceramic_pot"), M("planter_pot_clay"), { make: (s) => cart({ seed: s }), r: 2.2, w: 1 },
    { make: () => well(), r: 1.4, w: 0.5 }, M("wooden_crate_02")],
  street: [M("barrel_03"), M("wine_barrel_01", 0.9), M("wooden_crate_01"), M("wooden_crate_02"), M("ceramic_vase_01", 1.1), M("ceramic_vase_03"),
    M("wicker_basket_01"), M("wooden_bucket_01"), M("wooden_stool_01"), M("wooden_broom", 1, 0.3)],
  wallfoot: [M("rock_07", 0.6, 0.6), M("rock_09", 0.6, 0.6), M("moon_rock_02", 1.5), M("namaqualand_boulders_01", 0.4, 0.9), M("wicker_basket_01"),
    M("wooden_ladder", 1, 0.6), M("rusted_spade_01"), M("sledgehammer_01"), M("wooden_crate_01"), M("wooden_bucket_01")],
  workshop: [M("tree_stump_01", 0.8, 0.6), M("cross_pein_hammer"), M("sledgehammer_01"), M("wooden_bucket_01"), M("wooden_display_shelves_01", 1, 0.8),
    M("painted_wooden_table", 1, 1.0), M("brass_pot_01"), M("wooden_barrels_01", 0.8, 0.9), M("wooden_axe")],
  shore: [M("rock_07", 0.8, 0.8), M("namaqualand_boulders_01", 0.5, 1.0), M("barrel_03"), M("wooden_crate_02"), M("wicker_basket_02"),
    { make: () => palm(6), r: 1.2, w: 1 }],
};

/** scatter a preset over area [x0, z0, x1, z1] at floor y; n items; keep: actor spots and camera corridors */
export function fill(root: THREE.Object3D, preset: keyof typeof PRESETS | string, area: [number, number, number, number], o: { n?: number; y?: number; keep?: Box[]; seed?: number; face?: V3 } = {}): Box[] {
  const items = PRESETS[preset] ?? PRESETS.street, r = rng(o.seed ?? 11), placed: Box[] = [];
  const tot = items.reduce((a, b) => a + b.w, 0), y = o.y ?? 0;
  const pick = () => { let u = r() * tot; for (const it of items) { if ((u -= it.w) <= 0) return it; } return items[0]; };
  const free = (b: Box) => ![...(o.keep ?? []), ...placed].some((k) => b[0] < k[3] && b[3] > k[0] && b[2] < k[5] && b[5] > k[2]);
  const [x0, z0, x1, z1] = area;
  for (let i = 0, tries = 0; i < (o.n ?? 20) && tries < 600; tries++) {
    const it = pick(), x = x0 + r() * (x1 - x0), z = z0 + r() * (z1 - z0);
    const b: Box = [x - it.r, y, z - it.r, x + it.r, y + 3, z + it.r];
    if (!free(b)) continue;
    const m = it.make(Math.floor(r() * 1000)); m.position.set(x, y, z);
    m.rotation.y = o.face ? Math.atan2(o.face[0] - x, o.face[2] - z) + (r() - 0.5) * 0.6 : r() * Math.PI * 2;
    root.add(m); placed.push(b); i++;
  }
  return placed;
}

/** a readable crowd: n Actors in staggered rows across area, facing `face`, mixed costumes, faces and poses */
export function crowd(id: string, area: [number, number, number, number], n: number, o: { costumes: string[]; faces?: string[]; poses?: string[]; face?: V3; seed?: number; y?: number; spacing?: number }): PersonSpec[] {
  const r = rng(o.seed ?? 21), out: PersonSpec[] = [];
  const [x0, z0, x1, z1] = area, sp = o.spacing ?? 0.85;
  const cols = Math.max(1, Math.floor((x1 - x0) / sp)), rows = Math.ceil(n / cols);
  for (let i = 0; i < n; i++) {
    const c = i % cols, rw = Math.floor(i / cols);
    const x = x0 + (c + 0.5 + (rw % 2) * 0.5) * ((x1 - x0) / cols) + (r() - 0.5) * 0.25, z = z0 + ((rw + 0.5) / rows) * (z1 - z0) + (r() - 0.5) * 0.3;
    const p: V3 = [x, o.y ?? 0, z], costume = o.costumes[Math.floor(r() * o.costumes.length)];
    const face = (o.faces ?? ["focus", "worried", "frown", "neutral"])[Math.floor(r() * (o.faces?.length ?? 4))];
    const pose = (o.poses ?? ["stand", "hold", "hips", "point"])[Math.floor(r() * (o.poses?.length ?? 4))];
    const seed = Math.floor(r() * 1000);
    out.push({ id: `${id}${i}`, at: () => p, faceTo: o.face ? () => o.face! : undefined, scale: 0.94 + r() * 0.12, props: () => ({ costume, face, pose, seed }) });
  }
  return out;
}
