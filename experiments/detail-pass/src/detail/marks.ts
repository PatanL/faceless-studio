/**
 * Surface-mark generator (pure). Given a hero part's path and the scene light, it places CLUSTERED micro-marks
 * (scars, spot groups, dash clusters, pores, scale arcs, glints) inside the LIT region only, at value ±(6-10) %
 * of the base, seeded so marks never swim between frames.
 *
 * Lit region test is the exact complement of the engine's core-shadow mask (Shaded L1): a point p is lit when
 * p and p - key·coreDist are both inside the silhouette. Marks are also kept off the rim crescent and a margin
 * from the silhouette edge, so the silhouette itself never gets a dark rim of marks (outline response, D5).
 *
 * Clusters, not uniform sprinkles: Kurzgesagt's hero marks come in families (a patch of 5 spots with one big
 * centre spot, three parallel scars, a pore cloud). Cluster centres are Poisson-spaced with an acceptance bias
 * toward the terminator and the edges of forms, so the centre of the lit plane stays a little calmer.
 */
import {flatten, inside, polysBox, type Poly} from './pathgeo';
import {rng} from '../../../kurz-style/engine/src/lib/rng';

export type Vec = [number, number];
export type MarkKind = 'spots' | 'scar' | 'dash' | 'pores' | 'arcs' | 'glint';

export type MarkEl = {
	kind: MarkKind;
	/** shape primitive */
	prim: 'dot' | 'ring' | 'line' | 'curve' | 'arc' | 'bean';
	x: number;
	y: number;
	/** size (radius for dots/rings, length for lines) */
	s: number;
	/** angle in degrees */
	ang: number;
	/** value shift as a FRACTION of the base L (±0.06..0.10) */
	dv: number;
	/** inside the highlight plane (tone it from the highlight colour) */
	hi: boolean;
	cluster: number;
	w: number;
};

export type MarkOpts = {
	seed: string;
	d: string | string[];
	/** unit vector toward the key, in the part's LOCAL frame */
	key: Vec;
	/** unit vector toward the rim light, local frame */
	rim: Vec;
	/** form radius (same R as the Shaded group) */
	R: number;
	/** core-shadow distance as a fraction of R (Shaded default 0.38); ×1.15 safety so a light sweep never puts marks in shadow */
	core?: number;
	/** highlight crescent width as a fraction of R (Shaded default 0.22) */
	hiW?: number;
	rimW?: number;
	/** number of clusters */
	clusters: number;
	/** cluster kind weights */
	kinds: Partial<Record<MarkKind, number>>;
	/** base mark size in px */
	size: number;
	/** minimum distance between cluster centres, as a multiple of size (default 5) */
	spacing?: number;
	/** keep this far from the silhouette edge, px (default 1.2·size) */
	margin?: number;
	/** sign of the value shift: 'dark', 'light' or 'mixed' (default mixed, 65 % darker) */
	tone?: 'dark' | 'light' | 'mixed';
	/** optional extra exclusion (e.g. the eye) */
	exclude?: (x: number, y: number) => boolean;
};

const cache = new Map<string, MarkEl[]>();

export const placeMarks = (o: MarkOpts): MarkEl[] => {
	const key = JSON.stringify([o.seed, o.key.map((v) => v.toFixed(2)), o.clusters, o.size, typeof o.d === 'string' ? o.d.length : o.d.map((x) => x.length)]);
	const hit = cache.get(key);
	if (hit) return hit;
	const polys: Poly[] = (Array.isArray(o.d) ? o.d : [o.d]).flatMap((d) => flatten(d));
	const [bx, by, bw, bh] = polysBox(polys);
	const k = o.key;
	const rm = o.rim;
	const coreD = (o.core ?? 0.38) * 1.15 * o.R;
	const hiD = (o.hiW ?? 0.22) * o.R;
	const rimD = (o.rimW ?? Math.max(3, Math.min(9, 0.07 * o.R))) + 4;
	const margin = o.margin ?? o.size * 1.2;
	const ins = (x: number, y: number) => inside(polys, x, y);
	const safe = (x: number, y: number, m = margin) =>
		ins(x, y) && ins(x + m, y) && ins(x - m, y) && ins(x, y + m) && ins(x, y - m) && ins(x + rm[0] * (rimD + m), y + rm[1] * (rimD + m)) && !(o.exclude && o.exclude(x, y));
	const lit = (x: number, y: number) => ins(x - k[0] * coreD, y - k[1] * coreD);
	/** 0 deep in the lit plane .. 1 right at the terminator */
	const nearTerm = (x: number, y: number) => (ins(x - k[0] * coreD * 1.7, y - k[1] * coreD * 1.7) ? 0 : 1);
	const inHi = (x: number, y: number) => !ins(x + k[0] * hiD, y + k[1] * hiD);

	const r = rng(`marks:${o.seed}`);
	const kindsArr = Object.entries(o.kinds) as [MarkKind, number][];
	const wsum = kindsArr.reduce((a, [, w]) => a + w, 0);
	const pickKind = (): MarkKind => {
		let u = r() * wsum;
		for (const [kd, w] of kindsArr) {
			u -= w;
			if (u <= 0) return kd;
		}
		return kindsArr[0][0];
	};
	const spacing = (o.spacing ?? 5) * o.size;
	const centres: [number, number, MarkKind][] = [];
	for (let tries = 0; tries < o.clusters * 160 && centres.length < o.clusters; tries++) {
		const x = bx + r() * bw;
		const y = by + r() * bh;
		if (!safe(x, y) || !lit(x, y)) continue;
		// acceptance: favour the terminator band and form edges, keep the middle of the lit plane calmer
		const edge = safe(x, y, margin * 3.5) ? 0 : 1;
		const acc = 0.35 + 0.4 * nearTerm(x, y) + 0.25 * edge;
		if (r() > acc) continue;
		if (centres.some(([cx, cy]) => Math.hypot(cx - x, cy - y) < spacing)) continue;
		let kd = pickKind();
		for (let g = 0; kd === 'glint' && g < 20; g++) kd = pickKind();
		if (kd === 'glint') continue;
		centres.push([x, y, kd]);
	}
	// glints get their own pass: they belong in the highlight plane, which a uniform search rarely hits
	const wg = o.kinds.glint ?? 0;
	const ng = wg > 0 ? Math.max(1, Math.round((o.clusters * wg) / wsum)) : 0;
	for (let tries = 0, got = 0; tries < 4000 && got < ng; tries++) {
		const x = bx + r() * bw;
		const y = by + r() * bh;
		if (!safe(x, y) || !lit(x, y) || !inHi(x, y)) continue;
		if (centres.some(([cx, cy]) => Math.hypot(cx - x, cy - y) < spacing * 0.8)) continue;
		centres.push([x, y, 'glint']);
		got++;
	}

	const out: MarkEl[] = [];
	const sign = () => (o.tone === 'dark' ? -1 : o.tone === 'light' ? 1 : r() < 0.65 ? -1 : 1);
	const push = (el: Omit<MarkEl, 'hi'>) => {
		if (!safe(el.x, el.y, Math.max(2, el.prim === 'line' || el.prim === 'curve' ? el.s * 0.6 : el.s * 1.1))) return;
		if (!lit(el.x, el.y)) return;
		out.push({...el, hi: inHi(el.x, el.y)});
	};
	const S = o.size;
	centres.forEach(([cx, cy, kd], ci) => {
		const sg = sign();
		const dv = sg * (0.06 + r() * 0.04);
		const base = r() * 180;
		switch (kd) {
			case 'spots': {
				// one big centre spot (a ring: house motif) + 3-7 satellites, falling off in size
				const m = 3 + Math.floor(r() * 5);
				push({kind: kd, prim: 'ring', x: cx, y: cy, s: S * (0.75 + r() * 0.35), ang: 0, dv, cluster: ci, w: Math.max(1.6, S * 0.2)});
				for (let j = 0; j < m; j++) {
					const a = r() * Math.PI * 2;
					const dd = S * (1.3 + r() * 1.9);
					push({kind: kd, prim: 'dot', x: cx + Math.cos(a) * dd, y: cy + Math.sin(a) * dd * 0.8, s: S * (0.22 + r() * 0.3) * (1.2 - dd / (S * 4)), ang: 0, dv, cluster: ci, w: 0});
				}
				break;
			}
			case 'scar': {
				// 2-4 near-parallel healed scratches (rake marks)
				const m = 2 + Math.floor(r() * 3);
				const ang = base;
				const ux = Math.cos((ang * Math.PI) / 180);
				const uy = Math.sin((ang * Math.PI) / 180);
				const L = S * (2.6 + r() * 2);
				for (let j = 0; j < m; j++) {
					const off = (j - (m - 1) / 2) * S * 0.55;
					push({kind: kd, prim: 'curve', x: cx - uy * off + ux * (r() - 0.5) * S, y: cy + ux * off + uy * (r() - 0.5) * S, s: L * (0.7 + r() * 0.5), ang: ang + (r() - 0.5) * 10, dv, cluster: ci, w: Math.max(1.6, S * 0.16)});
				}
				break;
			}
			case 'dash': {
				const m = 3 + Math.floor(r() * 3);
				const ang = base;
				const ux = Math.cos((ang * Math.PI) / 180);
				const uy = Math.sin((ang * Math.PI) / 180);
				for (let j = 0; j < m; j++) {
					const off = j * S * 0.6;
					push({kind: kd, prim: 'line', x: cx - uy * off + ux * (r() - 0.5) * S * 0.6, y: cy + ux * off + uy * (r() - 0.5) * S * 0.6, s: S * (0.6 + r() * 0.7), ang: ang + (r() - 0.5) * 20, dv, cluster: ci, w: Math.max(2, S * 0.24)});
				}
				break;
			}
			case 'pores': {
				const m = 6 + Math.floor(r() * 9);
				for (let j = 0; j < m; j++) {
					const a = r() * Math.PI * 2;
					const dd = S * 1.6 * Math.sqrt(r());
					push({kind: kd, prim: 'dot', x: cx + Math.cos(a) * dd, y: cy + Math.sin(a) * dd, s: Math.max(1.3, S * (0.1 + r() * 0.12)), ang: 0, dv: dv * 1.1, cluster: ci, w: 0});
				}
				break;
			}
			case 'arcs': {
				// a short row of scale arcs
				const m = 3 + Math.floor(r() * 4);
				const ang = base;
				const ux = Math.cos((ang * Math.PI) / 180);
				const uy = Math.sin((ang * Math.PI) / 180);
				for (let j = 0; j < m; j++) {
					const row = j % 2;
					push({kind: kd, prim: 'arc', x: cx + ux * (j - m / 2) * S * 0.7 - uy * row * S * 0.5, y: cy + uy * (j - m / 2) * S * 0.7 + ux * row * S * 0.5, s: S * 0.55, ang, dv, cluster: ci, w: Math.max(1.5, S * 0.14)});
				}
				break;
			}
			case 'glint': {
				// wet-sheen glints: a bean + 1-2 satellites, always lighter
				const a = (Math.atan2(k[1], k[0]) * 180) / Math.PI + 90;
				push({kind: kd, prim: 'bean', x: cx, y: cy, s: S * (0.7 + r() * 0.5), ang: a, dv: 0.5, cluster: ci, w: 0});
				const m = 1 + Math.floor(r() * 2);
				for (let j = 0; j < m; j++) push({kind: kd, prim: 'dot', x: cx - k[1] * S * (1.2 + j), y: cy + k[0] * S * (1.2 + j), s: S * 0.18, ang: 0, dv: 0.5, cluster: ci, w: 0});
				break;
			}
		}
	});
	cache.set(key, out);
	return out;
};

export const countByKind = (els: MarkEl[]) => els.reduce<Record<string, number>>((a, e) => ((a[e.kind] = (a[e.kind] ?? 0) + 1), a), {});
