/**
 * Fish species as parametric silhouettes (pure geometry). Seven body plans, all drawn fresh from general
 * fish anatomy (no reference frames): a fusiform scad, a disc-bodied tang, a needle-snouted lancer, a boxy
 * trunkfish, a lyre-tailed anthias, a cigar wrasse and a striped grunt. Each fish instance gets per-fish
 * variation (depth, peak, tail size, fin height, colour drift, pattern phase), so no two fish in a school are
 * the same stamp.
 *
 * Local frame: nose at +50, tail base at -50, body length 100 units, back up (-y).
 */
import {closedSpline, openSpline} from '../../../kurz-style/engine/src/lib/geom';
import {rng} from '../../../kurz-style/engine/src/lib/rng';
import type {Pt} from './pathgeo';

export type TailKind = 'fork' | 'lunate' | 'round' | 'lyre' | 'notch';
export type Pattern = 'none' | 'stripe' | 'band' | 'stripes' | 'spots' | 'bars' | 'mask';

export type Species = {
	name: string;
	depth: number;
	peak: number;
	ped: number;
	/** share of the depth above the midline */
	up: number;
	/** snout sharpness (1 blunt .. 3 pointed) */
	snout: number;
	tail: TailKind;
	tailSize: number;
	dorsal: [number, number, number];
	anal: [number, number, number];
	eye: [number, number, number];
	pattern: Pattern;
	body: string;
	back: string;
	belly: string;
	accent: string;
	alt: string;
};

export const SPECIES: Record<string, Species> = {
	scad: {name: 'scad', depth: 0.22, peak: 0.55, ped: 0.05, up: 0.5, snout: 1.6, tail: 'fork', tailSize: 0.34, dorsal: [0.3, 0.62, 0.09], anal: [0.18, 0.42, 0.06], eye: [0.86, -0.08, 0.045], pattern: 'stripe', body: 'sky-3', back: 'dusk-3', belly: 'bone-1', accent: 'amber-4', alt: 'tide-3'},
	tang: {name: 'tang', depth: 0.62, peak: 0.5, ped: 0.08, up: 0.52, snout: 1.4, tail: 'lunate', tailSize: 0.3, dorsal: [0.1, 0.78, 0.09], anal: [0.1, 0.6, 0.08], eye: [0.8, -0.12, 0.05], pattern: 'mask', body: 'amber-3', back: 'amber-2', belly: 'amber-4', accent: 'tide-4', alt: 'ochre-3'},
	lancer: {name: 'lancer', depth: 0.11, peak: 0.42, ped: 0.04, up: 0.5, snout: 3, tail: 'fork', tailSize: 0.2, dorsal: [0.12, 0.26, 0.08], anal: [0.1, 0.24, 0.07], eye: [0.84, -0.05, 0.03], pattern: 'band', body: 'sky-2', back: 'dusk-2', belly: 'bone-1', accent: 'tide-5', alt: 'sky-3'},
	trunk: {name: 'trunk', depth: 0.54, peak: 0.55, ped: 0.13, up: 0.5, snout: 1, tail: 'round', tailSize: 0.26, dorsal: [0.16, 0.24, 0.07], anal: [0.14, 0.22, 0.06], eye: [0.76, -0.16, 0.06], pattern: 'spots', body: 'amber-4', back: 'amber-3', belly: 'bone-1', accent: 'coral-2', alt: 'amber-5'},
	anthias: {name: 'anthias', depth: 0.34, peak: 0.56, ped: 0.06, up: 0.52, snout: 1.5, tail: 'lyre', tailSize: 0.4, dorsal: [0.28, 0.82, 0.13], anal: [0.22, 0.45, 0.1], eye: [0.85, -0.08, 0.05], pattern: 'stripe', body: 'coral-3', back: 'coral-2', belly: 'coral-4', accent: 'amber-4', alt: 'coral-4'},
	wrasse: {name: 'wrasse', depth: 0.25, peak: 0.5, ped: 0.1, up: 0.5, snout: 1.7, tail: 'round', tailSize: 0.22, dorsal: [0.22, 0.86, 0.06], anal: [0.18, 0.5, 0.05], eye: [0.87, -0.1, 0.04], pattern: 'band', body: 'kelp-3', back: 'kelp-2', belly: 'kelp-4', accent: 'tide-4', alt: 'tide-2'},
	grunt: {name: 'grunt', depth: 0.36, peak: 0.55, ped: 0.08, up: 0.52, snout: 1.4, tail: 'notch', tailSize: 0.28, dorsal: [0.32, 0.78, 0.14], anal: [0.2, 0.4, 0.09], eye: [0.84, -0.12, 0.05], pattern: 'stripes', body: 'bone-1', back: 'ochre-3', belly: 'bone-2', accent: 'amber-3', alt: 'ochre-4'},
};

export type FishGeom = {
	body: string;
	back: string;
	belly: string;
	tail: string;
	dorsal: string;
	anal: string;
	pec: string;
	gill: string;
	/** lit edge along the back, toward the key */
	hiLine: string;
	pattern: {d: string; stroke?: number}[];
	eye: [number, number, number];
	/** colour drift toward the species alt colour, 0..0.35 */
	drift: number;
};

const P = (x: number, y: number): Pt => [x, y];

/** body + fins for one fish (per-fish variation from the seed) */
export const fishGeom = (sp: Species, seed: string): FishGeom => {
	const r = rng(`fish:${sp.name}:${seed}`);
	const D = sp.depth * (0.9 + r() * 0.22) * 100;
	const peak = Math.min(0.7, Math.max(0.35, sp.peak + (r() - 0.5) * 0.08));
	const q = Math.log(0.5) / Math.log(peak);
	const ped = sp.ped * 100;
	const prof = (s: number) => {
		const f = Math.pow(Math.sin(Math.PI * Math.pow(s, q)), 0.85);
		// pointed snout: thin the last 15 %
		const sn = s > 0.85 ? Math.pow(1 - (s - 0.85) / 0.15, (sp.snout - 1) * 0.6) : 1;
		return Math.max(s > 0.97 ? 0.4 : ped, (ped + (D - ped) * f) * sn);
	};
	const N = 10;
	const X = (s: number) => -50 + s * 100;
	const upP: Pt[] = [];
	const loP: Pt[] = [];
	for (let i = 0; i <= N; i++) {
		const s = i / N;
		const h = prof(s);
		upP.push(P(X(s), -h * sp.up));
		loP.push(P(X(s), h * (1 - sp.up)));
	}
	const outline = [...upP, P(51, (upP[N][1] + loP[N][1]) / 2), ...loP.slice().reverse()];
	const body = closedSpline(outline, 0.9);
	const mid = (k: number) => upP.map(([x, y], i) => P(x, y + (loP[i][1] - y) * k));
	const back = closedSpline([...upP, ...mid(0.42).reverse()], 0.9);
	const belly = closedSpline([...mid(0.72), ...loP.slice().reverse()], 0.9);

	// tail
	const ts = sp.tailSize * (0.85 + r() * 0.3) * 100;
	const ph = ped * 0.9;
	let tail: string;
	switch (sp.tail) {
		case 'fork':
			tail = closedSpline([P(-48, -ph), P(-50 - ts * 0.7, -ts * 0.75), P(-50 - ts * 0.95, -ts * 0.85), P(-50 - ts * 0.55, -ts * 0.15), P(-50 - ts * 0.38, 0), P(-50 - ts * 0.55, ts * 0.15), P(-50 - ts * 0.95, ts * 0.85), P(-50 - ts * 0.7, ts * 0.75), P(-48, ph)], 0.6);
			break;
		case 'lyre':
			tail = closedSpline([P(-48, -ph), P(-50 - ts * 0.6, -ts * 0.5), P(-50 - ts * 1.25, -ts * 0.95), P(-50 - ts * 0.6, -ts * 0.18), P(-50 - ts * 0.45, 0), P(-50 - ts * 0.6, ts * 0.18), P(-50 - ts * 1.25, ts * 0.95), P(-50 - ts * 0.6, ts * 0.5), P(-48, ph)], 0.6);
			break;
		case 'lunate':
			tail = closedSpline([P(-48, -ph), P(-50 - ts * 0.55, -ts * 0.6), P(-50 - ts * 0.85, -ts * 0.95), P(-50 - ts * 0.6, -ts * 0.3), P(-50 - ts * 0.55, 0), P(-50 - ts * 0.6, ts * 0.3), P(-50 - ts * 0.85, ts * 0.95), P(-50 - ts * 0.55, ts * 0.6), P(-48, ph)], 0.7);
			break;
		case 'notch':
			tail = closedSpline([P(-48, -ph), P(-50 - ts * 0.7, -ts * 0.62), P(-50 - ts * 0.9, -ts * 0.5), P(-50 - ts * 0.72, 0), P(-50 - ts * 0.9, ts * 0.5), P(-50 - ts * 0.7, ts * 0.62), P(-48, ph)], 0.7);
			break;
		default:
			tail = closedSpline([P(-48, -ph), P(-50 - ts * 0.5, -ts * 0.55), P(-50 - ts * 0.95, -ts * 0.3), P(-50 - ts, 0), P(-50 - ts * 0.95, ts * 0.3), P(-50 - ts * 0.5, ts * 0.55), P(-48, ph)], 0.9);
	}

	const fin = (from: number, to: number, hgt: number, top: boolean): string => {
		const h = hgt * (0.8 + r() * 0.45) * 100;
		const prof2 = top ? upP : loP;
		const at = (s: number): Pt => {
			const i = Math.min(N - 1, Math.floor(s * N));
			const f = s * N - i;
			return P(prof2[i][0] + (prof2[i + 1][0] - prof2[i][0]) * f, prof2[i][1] + (prof2[i + 1][1] - prof2[i][1]) * f);
		};
		const a = at(from);
		const b = at(to);
		const sg = top ? -1 : 1;
		const pts: Pt[] = [P(a[0] - 2, a[1] - sg * 2)];
		const m = 5;
		for (let i = 0; i <= m; i++) {
			const s = from + ((to - from) * i) / m;
			const base = at(s);
			// rays: a soft scalloped edge, tallest near the front third (spiny dorsal)
			const env = Math.sin(Math.PI * Math.min(1, (i / m) * 1.1 + 0.05)) * (1 - 0.35 * (i / m));
			pts.push(P(base[0] - h * 0.25, base[1] + sg * h * (0.4 + 0.6 * env) * (i % 2 ? 0.88 : 1)));
		}
		pts.push(P(b[0] + 2, b[1] - sg * 2));
		return closedSpline(pts.reverse(), 0.7);
	};
	const dorsal = fin(sp.dorsal[0], sp.dorsal[1], sp.dorsal[2], true);
	const anal = fin(sp.anal[0], sp.anal[1], sp.anal[2], false);

	const ex = X(sp.eye[0]);
	const eyR = sp.eye[2] * 100 * (0.9 + r() * 0.2);
	const hAt = prof(sp.eye[0]);
	const ey = sp.eye[1] * hAt * 2 + (-hAt * sp.up + hAt * (1 - sp.up)) / 2;
	const pecL = D * 0.32;
	const px = ex - eyR * 3.2;
	const py = ey + hAt * 0.55;
	const pec = closedSpline([P(px, py - 2), P(px - pecL, py - pecL * 0.2), P(px - pecL * 0.9, py + pecL * 0.35), P(px, py + 3)], 0.8);
	const gs = Math.max(0.55, sp.eye[0] - 0.12);
	const gx = X(gs);
	const gh = prof(gs);
	const gill = openSpline([P(gx + 3, -gh * sp.up * 0.7), P(gx - 2, 0), P(gx + 2, gh * (1 - sp.up) * 0.7)], 1);

	const hiLine = openSpline(upP.slice(2, N - 1).map(([x, y], i) => P(x, y + prof((i + 2) / N) * 0.2)), 1);
	const pattern: FishGeom['pattern'] = [];
	const k0 = r();
	switch (sp.pattern) {
		case 'stripe': {
			const yy = (s: number) => {
				const h = prof(s);
				return -h * sp.up + h * (0.36 + 0.06 * k0);
			};
			pattern.push({d: openSpline([0.12, 0.35, 0.6, 0.82].map((s) => P(X(s), yy(s))), 1), stroke: Math.max(2.2, D * 0.07)});
			break;
		}
		case 'band': {
			const yy = (s: number) => {
				const h = prof(s);
				return -h * sp.up + h * 0.5;
			};
			pattern.push({d: openSpline([0.05, 0.3, 0.6, 0.9].map((s) => P(X(s), yy(s))), 1), stroke: Math.max(2.4, D * 0.16)});
			break;
		}
		case 'stripes':
			for (let j = 0; j < 3; j++) {
				const f = 0.22 + j * 0.2 + (k0 - 0.5) * 0.05;
				const yy = (s: number) => {
					const h = prof(s);
					return -h * sp.up + h * f;
				};
				pattern.push({d: openSpline([0.08, 0.35, 0.62, 0.86].map((s) => P(X(s), yy(s))), 1), stroke: Math.max(2, D * 0.06)});
			}
			break;
		case 'spots': {
			const m = 5 + Math.floor(r() * 4);
			for (let j = 0; j < m; j++) {
				const s = 0.2 + r() * 0.55;
				const h = prof(s);
				const y = -h * sp.up + h * (0.2 + r() * 0.55);
				const rr = 2 + r() * 2.5;
				pattern.push({d: `M ${X(s) - rr} ${y} A ${rr} ${rr} 0 1 0 ${X(s) + rr} ${y} A ${rr} ${rr} 0 1 0 ${X(s) - rr} ${y} Z`});
			}
			break;
		}
		case 'mask': {
			// a soft vertical band behind the eye
			const s0 = sp.eye[0] - 0.12;
			const pts = [s0 - 0.04, s0 + 0.04].map((s) => {
				const h = prof(s);
				return [P(X(s), -h * sp.up * 0.92), P(X(s), h * (1 - sp.up) * 0.92)];
			});
			pattern.push({d: closedSpline([pts[0][0], pts[1][0], pts[1][1], pts[0][1]], 0.6)});
			break;
		}
		default:
			break;
	}
	return {body, back, belly, tail, dorsal, anal, pec, gill, hiLine, pattern, eye: [ex, ey, eyR], drift: r() * 0.35};
};

/** distant eagle-ray silhouette (local, nose +x), wing phase 0..1 */
export const raySil = (flap: number): string => {
	const w = 60 * (0.8 + 0.25 * Math.sin(flap * Math.PI * 2));
	const tipY = 4 * Math.sin(flap * Math.PI * 2 + 1);
	return closedSpline(
		[
			P(40, 0),
			P(26, -10),
			P(-2, -w * 0.7),
			P(-12, -w + tipY),
			P(-16, -w * 0.6),
			P(-30, -6),
			P(-46, -1),
			P(-110, 0),
			P(-46, 1),
			P(-30, 6),
			P(-16, w * 0.6),
			P(-12, w - tipY),
			P(-2, w * 0.7),
			P(26, 10),
		],
		0.7,
	);
};
