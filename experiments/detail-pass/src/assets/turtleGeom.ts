/**
 * Hero: a sea turtle in a three-quarter dorsal view, swimming left (pure geometry; drawn fresh from turtle
 * anatomy, not from any reference frame). Local frame, about 610 x 450 units.
 *
 *   carapace  tapered ellipse; 5 vertebral, 2x4 costal and 24 marginal scutes built procedurally from
 *             x-bands of the inner ellipse, so the seams always meet; tortoiseshell streak wedges and
 *             growth rings per scute
 *   skin      head + neck, 2 front flippers (power stroke with follow-through: the tip rotates more than the
 *             root), 2 rear flippers, tail, plastron; a jittered hex tessellation of dark scales on pale skin
 *   marks     placeMarks() clusters on the carapace, head and both near flippers (lit side only)
 */
import {blob, closedSpline, taper} from '../../../kurz-style/engine/src/lib/geom';
import {rng} from '../../../kurz-style/engine/src/lib/rng';
import {centroid, flatten, inside, polyPath, scalePoly, type Poly, type Pt} from '../detail/pathgeo';
import {placeMarks, type MarkEl, type Vec} from '../detail/marks';

export const CX = 350;
export const CY = 200;
export const RX = 215;
export const RY = 122;

const shellPt = (th: number, rho: number): Pt => [CX + rho * RX * Math.cos(th) * (1 + 0.04 * Math.cos(th)), CY + rho * RY * Math.sin(th) * (1 - 0.1 * Math.cos(th))];

const ring = (rho: number, n = 72): Pt[] => Array.from({length: n}, (_, i) => shellPt((i / n) * Math.PI * 2, rho));

export const SHELL = closedSpline(ring(1, 40), 1);

/** y of the inner ellipse's upper / lower chain at x (linear interp over a dense sample) */
const chain = (rho: number, upper: boolean): ((x: number) => number) => {
	const pts: Pt[] = [];
	for (let i = 0; i <= 120; i++) {
		const th = Math.PI + (i / 120) * Math.PI * (upper ? 1 : -1);
		pts.push(shellPt(th, rho));
	}
	pts.sort((a, b) => a[0] - b[0]);
	return (x: number) => {
		if (x <= pts[0][0]) return pts[0][1];
		for (let i = 1; i < pts.length; i++)
			if (x <= pts[i][0]) {
				const f = (x - pts[i - 1][0]) / (pts[i][0] - pts[i - 1][0] || 1);
				return pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * f;
			}
		return pts[pts.length - 1][1];
	};
};

const RHO = 0.84;
const yIU = chain(RHO, true);
const yIL = chain(RHO, false);
const yMid = (x: number) => CY - 0.24 * RY + 0.04 * (x - CX) * 0.1;

const r0 = rng('turtle-shell');
const VX: number[] = (() => {
	const a = CX - 0.8 * RX;
	const b = CX + 0.8 * RX;
	const v = [a];
	for (let i = 1; i < 5; i++) v.push(a + ((b - a) * i) / 5 + (r0() - 0.5) * 12);
	v.push(b);
	return v;
})();
const vertHalf = (x: number) => {
	let i = 0;
	while (i < 4 && x > VX[i + 1]) i++;
	const f = (x - VX[i]) / (VX[i + 1] - VX[i]);
	const env = Math.sqrt(Math.max(0, 1 - Math.pow((x - CX) / (0.86 * RX), 2)));
	const tip = Math.min(1, Math.max(0, (x - VX[0]) / 30), Math.max(0, (VX[5] - x) / 30));
	return 0.27 * RY * Math.pow(env, 0.5) * (0.8 + 0.2 * Math.sin(Math.PI * f)) * Math.sqrt(tip);
};
const vUp = (x: number) => Math.max(yIU(x) + 3, yMid(x) - vertHalf(x));
const vLo = (x: number) => Math.min(yIL(x) - 3, yMid(x) + vertHalf(x) * 1.12);

/** sample a chain y(x) from xa to xb */
const along = (f: (x: number) => number, xa: number, xb: number, n = 8): Pt[] => Array.from({length: n + 1}, (_, i) => {
	const x = xa + ((xb - xa) * i) / n;
	return [x, f(x)] as Pt;
});

const XA = CX - RHO * RX * 1.03;
const XB = CX + RHO * RX * 1.03;
const inV = (x: number) => x > VX[0] && x < VX[5];
const topEdge = (x: number) => (inV(x) ? vUp(x) : yMid(x));
const botEdge = (x: number) => (inV(x) ? vLo(x) : yMid(x));

/** vertebral scutes: hexagon-ish plates along the dorsal ridge (wavy shared edges = pointed joints) */
export const VERTEBRAL: Pt[][] = Array.from({length: 5}, (_, i) => [...along(vUp, VX[i], VX[i + 1]), ...along(vLo, VX[i + 1], VX[i])]);

/** costal scutes: seams RADIATE from the vertebral joints out to the inner marginal ring */
const SEAMS_BOT = [XA, VX[1] + 4, (VX[2] + VX[3]) / 2 + 6, VX[4] - 4, XB];
const radiate = (x: number, k: number) => CX + (x - CX) * k;
const costal = (upper: boolean): Pt[][] =>
	Array.from({length: 4}, (_, j) => {
		const b0 = SEAMS_BOT[j];
		const b1 = SEAMS_BOT[j + 1];
		const t0 = j === 0 ? XA : radiate(b0, upper ? 1.22 : 1.3);
		const t1 = j === 3 ? XB : radiate(b1, upper ? 1.22 : 1.3);
		const inner = upper ? topEdge : botEdge;
		const outer = upper ? yIU : yIL;
		return [...along(inner, b0, b1), ...along(outer, t1, t0)];
	});
export const COSTAL: Pt[][] = [...costal(true), ...costal(false)];

const NM = 24;
export const MARGINAL: Pt[][] = Array.from({length: NM}, (_, k) => {
	const a = (k / NM) * Math.PI * 2 + 0.07;
	const b = ((k + 1) / NM) * Math.PI * 2 + 0.07;
	const m = (a + b) / 2;
	return [shellPt(a, 1.02), shellPt(m, 1.03), shellPt(b, 1.02), shellPt(b, RHO), shellPt(m, RHO - 0.006), shellPt(a, RHO)];
});

/** the seam network: every scute edge, stroked pale (no dark lines anywhere) */
export const SEAMS: string = [...VERTEBRAL, ...COSTAL, ...MARGINAL.map((p) => [p[2], p[3]] as Pt[])].map((p) => polyPath(p, p.length > 2)).join(' ');

const rs = rng('turtle-streaks');
/** tortoiseshell: per scute 1-2 rounded blotches + 2-4 short wedges radiating from the scute's rear growth centre */
export const STREAKS: {dark: string[]; light: string[]} = (() => {
	const dark: string[] = [];
	const light: string[] = [];
	for (const p of [...VERTEBRAL, ...COSTAL]) {
		const [cx, cy] = centroid(p);
		const xs = p.map((q) => q[0]);
		const ys = p.map((q) => q[1]);
		const w = Math.max(...xs) - Math.min(...xs);
		const h = Math.max(...ys) - Math.min(...ys);
		if (w < 18 || h < 14) continue;
		const ox = cx + w * 0.22;
		const oy = cy + (rs() - 0.5) * h * 0.2;
		const n = 2 + Math.floor(rs() * 3);
		for (let i = 0; i < n; i++) {
			const ang = Math.PI + (i / Math.max(1, n - 1) - 0.5) * 1.5 + (rs() - 0.5) * 0.3;
			const len = Math.min(w, h * 1.6) * (0.3 + rs() * 0.25);
			const pts: Pt[] = [
				[ox, oy],
				[ox + Math.cos(ang) * len * 0.55, oy + Math.sin(ang) * len * 0.5],
				[ox + Math.cos(ang) * len, oy + Math.sin(ang) * len * 0.9],
			];
			(i % 3 === 2 ? light : dark).push(taper(pts, 6 + rs() * 6, 1.5));
		}
		const nb = 1 + Math.floor(rs() * 2);
		for (let i = 0; i < nb; i++) {
			const bx = cx + (rs() - 0.6) * w * 0.5;
			const by = cy + (rs() - 0.5) * h * 0.45;
			(rs() < 0.7 ? dark : light).push(blob(`tb${dark.length}${i}`, bx, by, Math.min(w, h) * (0.12 + rs() * 0.1), Math.min(w, h) * (0.08 + rs() * 0.06), {n: 7, jag: 0.35}));
		}
	}
	return {dark, light};
})();
/** growth rings: two rounded concentric rings per scute, toward the rear growth centre */
export const GROWTH: string = [...VERTEBRAL, ...COSTAL]
	.flatMap((p) => {
		const [cx, cy] = centroid(p);
		const xs = p.map((q) => q[0]);
		const o: Pt = [cx + (Math.max(...xs) - Math.min(...xs)) * 0.12, cy];
		return [0.62].map((k) => closedSpline(scalePoly(p.filter((_, i) => i % 2 === 0), k, o), 0.8));
	})
	.join(' ');
export const polysD = (ps: Pt[][]) => ps.map((p) => polyPath(p)).join(' ');

// ---------------------------------------------------------------- skin

export type Limb = {name: string; pivot: Pt; pts: Pt[]; w0: number; w1: number; cell: number};
export const LIMBS: Limb[] = [
	{name: 'farFront', pivot: [215, 142], pts: [[215, 142], [248, 100], [290, 62], [334, 30], [372, 12]], w0: 64, w1: 10, cell: 17},
	{name: 'farRear', pivot: [520, 132], pts: [[520, 132], [552, 112], [580, 100], [604, 96]], w0: 36, w1: 10, cell: 14},
	{name: 'nearRear', pivot: [505, 282], pts: [[505, 282], [536, 312], [566, 330], [594, 338]], w0: 54, w1: 14, cell: 15},
	{name: 'nearFront', pivot: [205, 268], pts: [[205, 268], [238, 314], [280, 358], [326, 394], [372, 416]], w0: 82, w1: 12, cell: 19},
];
export const TAIL = taper(
	[
		[552, 204],
		[584, 210],
		[606, 216],
	],
	24,
	4,
);
export const PLASTRON = closedSpline(
	[
		[190, 262],
		[300, 296],
		[420, 300],
		[520, 268],
		[500, 250],
		[350, 262],
		[210, 248],
	],
	0.8,
);
export const HEAD_PIVOT: Pt = [168, 214];
export const HEAD_PTS: Pt[] = [
	[178, 178],
	[140, 170],
	[104, 166],
	[70, 166],
	[40, 174],
	[18, 190],
	[6, 210],
	[12, 225],
	[32, 237],
	[62, 245],
	[100, 250],
	[140, 258],
	[180, 262],
];
export const HEAD = closedSpline(HEAD_PTS, 0.9);
export const EYE: [number, number, number] = [60, 198, 11];
export const MOUTH = 'M 10 222 Q 30 233 58 233';
/** horny beak sheath (lighter sub-form) and the brow plate over the eye */
export const BEAK = 'M 6 210 C 10 196 22 188 32 192 C 30 206 30 222 34 236 C 22 234 12 228 6 218 Z';
export const BROW = 'M 44 190 Q 60 180 78 190';

/** limb pose at time t: rotation in degrees at the root, growing toward the tip (follow-through) */
export const limbAngle = (name: string, t: number): number => {
	const f = 0.34;
	const w = 2 * Math.PI * f * t;
	switch (name) {
		case 'nearFront':
			return 15 * Math.sin(w);
		case 'farFront':
			return -13 * Math.sin(w - 0.25);
		case 'nearRear':
			return 9 * Math.sin(w + 1.3);
		case 'farRear':
			return -7 * Math.sin(w + 1.1);
		default:
			return 0;
	}
};
export const limbXf = (lb: Limb, deg: number) => {
	const L = Math.hypot(lb.pts[lb.pts.length - 1][0] - lb.pivot[0], lb.pts[lb.pts.length - 1][1] - lb.pivot[1]);
	return (x: number, y: number): Pt => {
		const s = Math.min(1.2, Math.hypot(x - lb.pivot[0], y - lb.pivot[1]) / L);
		const a = (deg * (0.65 + 0.7 * s) * Math.PI) / 180;
		const ca = Math.cos(a);
		const sa = Math.sin(a);
		return [lb.pivot[0] + (x - lb.pivot[0]) * ca - (y - lb.pivot[1]) * sa, lb.pivot[1] + (x - lb.pivot[0]) * sa + (y - lb.pivot[1]) * ca];
	};
};
export const limbPath = (lb: Limb, xf?: (x: number, y: number) => Pt) => taper(xf ? lb.pts.map(([x, y]) => xf(x, y)) : lb.pts, lb.w0, lb.w1);

/** jittered hex tessellation of scale cells inside a closed path (rest pose) */
const hexCells = (seed: string, d: string, cell: number, gap: number): Pt[][] => {
	const polys: Poly[] = flatten(d);
	const xs = polys.flat().map((p) => p[0]);
	const ys = polys.flat().map((p) => p[1]);
	const x0 = Math.min(...xs);
	const x1 = Math.max(...xs);
	const y0 = Math.min(...ys);
	const y1 = Math.max(...ys);
	const r = rng(`hex:${seed}`);
	const out: Pt[][] = [];
	const dy = cell * 0.866;
	for (let j = 0, y = y0; y <= y1 + cell; j++, y += dy)
		for (let x = x0 + (j % 2 ? cell / 2 : 0); x <= x1 + cell; x += cell) {
			const cx = x + (r() - 0.5) * cell * 0.25;
			const cy = y + (r() - 0.5) * cell * 0.25;
			if (!inside(polys, cx, cy)) continue;
			const s = cell * (0.5 + r() * 0.12) - gap;
			const rot = r() * 0.4;
			const p: Pt[] = [];
			for (let k = 0; k < 6; k++) {
				const a = rot + (k / 6) * Math.PI * 2;
				const q = s * (0.88 + r() * 0.2);
				p.push([cx + Math.cos(a) * q, cy + Math.sin(a) * q * 0.9]);
			}
			out.push(p);
		}
	return out;
};
export const cellPath = (p: Pt[]) => closedSpline(p, 0.7);

export const LIMB_CELLS: Record<string, Pt[][]> = Object.fromEntries(LIMBS.map((lb) => [lb.name, hexCells(lb.name, limbPath(lb), lb.cell, 2.2)]));
export const HEAD_CELLS: Pt[][] = hexCells('head', HEAD, 25, 2.6).filter((p) => {
	const [x, y] = centroid(p);
	return x > 38 && Math.hypot(x - EYE[0], y - EYE[1]) > EYE[2] * 2.2;
});

// ---------------------------------------------------------------- hero marks (rest pose, reference light)

export type HeroMarks = {shell: MarkEl[]; head: MarkEl[]; nearFront: MarkEl[]; nearRear: MarkEl[]};

export const heroMarks = (keyLocal: Vec, rimLocal: Vec): HeroMarks => ({
	shell: placeMarks({
		seed: 'turtle-shell',
		d: SHELL,
		key: keyLocal,
		rim: rimLocal,
		R: RY,
		clusters: 16,
		kinds: {scar: 2.5, spots: 2.5, pores: 1.5, dash: 2.5, arcs: 1, glint: 2},
		size: 7,
		spacing: 4.5,
	}),
	head: placeMarks({
		seed: 'turtle-head',
		d: HEAD,
		key: keyLocal,
		rim: rimLocal,
		R: 42,
		clusters: 4,
		kinds: {spots: 3, pores: 2, glint: 1},
		size: 5,
		spacing: 3.5,
		exclude: (x, y) => Math.hypot(x - EYE[0], y - EYE[1]) < EYE[2] * 1.8,
	}),
	nearFront: placeMarks({seed: 'turtle-nf', d: limbPath(LIMBS[3]), key: keyLocal, rim: rimLocal, R: 30, clusters: 4, kinds: {spots: 2, scar: 1, pores: 2}, size: 5, spacing: 3.5}),
	nearRear: placeMarks({seed: 'turtle-nr', d: limbPath(LIMBS[2]), key: keyLocal, rim: rimLocal, R: 22, clusters: 2, kinds: {spots: 1, pores: 2}, size: 4.5, spacing: 3}),
});

export const TURTLE_BOX: [number, number, number, number] = [0, 0, 612, 430];
