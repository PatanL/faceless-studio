/**
 * Environment scatter (pure). Places seeded, varied object sets per depth plane with density rules:
 *
 *   families   each anchor (a big rock, brain coral, vase sponge, table coral, antler coral) gets 2-6 smaller
 *              satellites around it (tubes, ball sponges, soft coral, grass, urchins, stars, shells), the
 *              way reefs actually clump; singletons fill the gaps at a lower rate
 *   edge bias  anchor x is drawn from p(u) ∝ (1 - e) + e·|2u - 1|^1.2, so mass gathers toward the frame
 *              edges and the centre stays readable (bible §7.2, KB §7)
 *   calm field an ellipse (30-50 % of the frame) where nothing is placed; objects near its feathered edge
 *              are rejected with probability = calm weight, measured at the object's TOP, so tall things
 *              never poke into it
 *   depth      a y band below the ground line; deeper rows are scaled up (perspective) and drawn later
 *   spacing    anchors keep (s_i + s_j)·gap/2 apart in x within the same depth row
 *
 * Output is a flat list of placements, sorted back to front, that the React layer maps to generators and the
 * manifest script counts.
 */
import {rng} from '../../../kurz-style/engine/src/lib/rng';

export type Calm = {cx: number; cy: number; rx: number; ry: number; feather: number};

export const calmWeight = (c: Calm | undefined, x: number, y: number): number => {
	if (!c) return 0;
	const d = Math.hypot((x - c.cx) / c.rx, (y - c.cy) / c.ry);
	if (d <= 1) return 1;
	if (d >= 1 + c.feather) return 0;
	return 1 - (d - 1) / c.feather;
};

/** share of the W x H frame inside the calm ellipse (core, not feather) */
export const calmShare = (c: Calm, W: number, H: number): number => {
	let n = 0;
	let k = 0;
	for (let y = 4; y < H; y += 8)
		for (let x = 4; x < W; x += 8) {
			k++;
			if (Math.hypot((x - c.cx) / c.rx, (y - c.cy) / c.ry) <= 1) n++;
		}
	return n / k;
};

export type KindSpec = {kind: string; w: number; size: [number, number]; tall?: number};

export type Placement = {id: string; kind: string; x: number; y: number; size: number; seed: string; plane: string; z: number; variant: number};

export type GroundSpec = {
	seed: string;
	plane: string;
	x0: number;
	x1: number;
	/** ground line y at x */
	groundY: (x: number) => number;
	/** rows below the ground line, px */
	depth: number;
	anchors: number;
	satellites: [number, number];
	singles: number;
	anchorKinds: KindSpec[];
	satKinds: KindSpec[];
	edgeBias: number;
	calm?: Calm;
	gap?: number;
	/** perspective scale gain from the back row to the front row */
	persp?: number;
};

const pick = (r: () => number, ks: KindSpec[]): KindSpec => {
	const s = ks.reduce((a, k) => a + k.w, 0);
	let u = r() * s;
	for (const k of ks) {
		u -= k.w;
		if (u <= 0) return k;
	}
	return ks[ks.length - 1];
};

export const scatterGround = (g: GroundSpec): Placement[] => {
	const r = rng(`scatter:${g.seed}`);
	const out: Placement[] = [];
	const gap = g.gap ?? 0.8;
	const persp = g.persp ?? 0.35;
	const sampleX = () => {
		for (let i = 0; i < 64; i++) {
			const u = r();
			const p = 1 - g.edgeBias + g.edgeBias * Math.pow(Math.abs(2 * u - 1), 1.2);
			if (r() < p) return g.x0 + u * (g.x1 - g.x0);
		}
		return g.x0 + r() * (g.x1 - g.x0);
	};
	const ok = (x: number, y: number, size: number, tall: number) => r() >= calmWeight(g.calm, x, y - size * tall);
	let n = 0;
	const add = (k: KindSpec, x: number, dz: number, scale = 1) => {
		const y = g.groundY(x) + dz;
		const sz = (k.size[0] + r() * (k.size[1] - k.size[0])) * scale * (1 - persp / 2 + (persp * dz) / Math.max(1, g.depth));
		if (!ok(x, y, sz, k.tall ?? 0.8)) return null;
		const p: Placement = {id: `${g.seed}-${n++}`, kind: k.kind, x, y, size: sz, seed: `${g.seed}${n}`, plane: g.plane, z: dz, variant: r()};
		out.push(p);
		return p;
	};
	const anchors: Placement[] = [];
	for (let i = 0, tries = 0; i < g.anchors && tries < g.anchors * 30; tries++) {
		const k = pick(r, g.anchorKinds);
		const x = sampleX();
		const dz = r() * g.depth * 0.7;
		const sz = (k.size[0] + k.size[1]) / 2;
		if (anchors.some((a) => Math.abs(a.x - x) < (a.size + sz) * gap * 0.5 && Math.abs(a.z - dz) < g.depth * 0.3)) continue;
		const a = add(k, x, dz);
		if (!a) continue;
		anchors.push(a);
		i++;
		const ns = g.satellites[0] + Math.floor(r() * (g.satellites[1] - g.satellites[0] + 1));
		for (let j = 0; j < ns; j++) {
			const sk = pick(r, g.satKinds);
			const side = r() < 0.5 ? -1 : 1;
			const sx = a.x + side * a.size * (0.45 + r() * 0.75);
			add(sk, Math.max(g.x0, Math.min(g.x1, sx)), Math.min(g.depth, a.z + (r() - 0.3) * g.depth * 0.35), 0.85 + r() * 0.3);
		}
	}
	for (let i = 0; i < g.singles; i++) add(pick(r, g.satKinds), g.x0 + r() * (g.x1 - g.x0), r() * g.depth);
	return out.sort((a, b) => a.z - b.z);
};

/** a kelp grove: n strands around x with varied height, lean and curvature */
export type KelpP = {id: string; x: number; y: number; h: number; lean: number; bend: number; style: 'lance' | 'broad' | 'frond'; seed: string};
export const grove = (seed: string, x: number, y: number, n: number, h: [number, number], spread: number, lean: number): KelpP[] => {
	const r = rng(`grove:${seed}`);
	const styles: KelpP['style'][] = ['lance', 'broad', 'frond'];
	return Array.from({length: n}, (_, i) => ({
		id: `${seed}-${i}`,
		x: x + (r() - 0.5) * spread,
		y: y + r() * 30,
		h: h[0] + r() * (h[1] - h[0]),
		lean: lean + (r() - 0.5) * 16,
		bend: (r() - 0.5) * 40,
		style: styles[Math.floor(r() * 3)],
		seed: `${seed}${i}`,
	}));
};
