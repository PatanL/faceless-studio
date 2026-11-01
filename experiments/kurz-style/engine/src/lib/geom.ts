/**
 * Path helpers. Engine paths are written with ABSOLUTE commands and x,y pairs only (M L C Q Z), so they can
 * be measured and warped by rewriting their coordinate pairs.
 */
import {rng} from './rng';

export type Box = [number, number, number, number]; // x, y, w, h

const PAIR = /(-?\d*\.?\d+(?:e-?\d+)?)[ ,]+(-?\d*\.?\d+(?:e-?\d+)?)/g;

/** Approximate bounds from the path's points (control points included: slightly generous, never tight-low). */
export const pathBox = (...ds: string[]): Box => {
	let x0 = Infinity;
	let y0 = Infinity;
	let x1 = -Infinity;
	let y1 = -Infinity;
	for (const d of ds) {
		for (const m of d.matchAll(PAIR)) {
			const x = +m[1];
			const y = +m[2];
			x0 = Math.min(x0, x);
			y0 = Math.min(y0, y);
			x1 = Math.max(x1, x);
			y1 = Math.max(y1, y);
		}
	}
	return [x0, y0, x1 - x0, y1 - y0];
};

/** Rewrite every coordinate pair through f. */
export const warp = (d: string, f?: (x: number, y: number) => [number, number]): string =>
	f
		? d.replace(PAIR, (_, a, b) => {
				const [x, y] = f(+a, +b);
				return `${x.toFixed(1)} ${y.toFixed(1)}`;
			})
		: d;

/**
 * Travelling-wave body bend for swimmers (whale = vertical tail beat). Displacement grows from 0 at the
 * pivot (near the head) to `amp` at the tail tip, and lags along the body (the wave travels tailward).
 */
export const swimBend = (o: {head: number; tail: number; amp: number; t: number; freq: number; lag?: number; axis?: 'y' | 'x'}) => {
	const L = o.head - o.tail;
	const lag = o.lag ?? 1.6;
	return (x: number, y: number): [number, number] => {
		const s = Math.max(0, Math.min(1.15, (o.head - x) / L)); // 0 head .. 1 tail
		const env = Math.pow(Math.max(0, s - 0.18) / 0.82, 1.8);
		const d = o.amp * env * Math.sin(2 * Math.PI * o.freq * o.t - lag * s);
		return o.axis === 'x' ? [x + d, y] : [x, y + d];
	};
};

/** Smooth closed path through points (Catmull-Rom -> cubic Bezier). */
export const closedSpline = (pts: [number, number][], tension = 1): string => {
	const n = pts.length;
	let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
	for (let i = 0; i < n; i++) {
		const p0 = pts[(i - 1 + n) % n];
		const p1 = pts[i];
		const p2 = pts[(i + 1) % n];
		const p3 = pts[(i + 2) % n];
		const k = tension / 6;
		const c1: [number, number] = [p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k];
		const c2: [number, number] = [p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k];
		d += ` C ${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
	}
	return d + ' Z';
};

/** Open smooth path through points. */
export const openSpline = (pts: [number, number][], tension = 1): string => {
	const n = pts.length;
	let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)}`;
	for (let i = 0; i < n - 1; i++) {
		const p0 = pts[Math.max(0, i - 1)];
		const p1 = pts[i];
		const p2 = pts[i + 1];
		const p3 = pts[Math.min(n - 1, i + 2)];
		const k = tension / 6;
		d += ` C ${(p1[0] + (p2[0] - p0[0]) * k).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) * k).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) * k).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) * k).toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
	}
	return d;
};

/** Seeded organic blob (rocks, sponges): n lobes around (cx, cy), flattened bottom optional. */
export const blob = (seed: string, cx: number, cy: number, rx: number, ry: number, o: {n?: number; jag?: number; flatBottom?: boolean} = {}): string => {
	const r = rng(seed);
	const n = o.n ?? 9;
	const jag = o.jag ?? 0.22;
	const pts: [number, number][] = [];
	for (let i = 0; i < n; i++) {
		const a = (i / n) * Math.PI * 2 + (r() - 0.5) * 0.35;
		const k = 1 - jag / 2 + r() * jag;
		let y = cy + Math.sin(a) * ry * k;
		if (o.flatBottom && y > cy + ry * 0.55) y = cy + ry * 0.55 + (y - cy - ry * 0.55) * 0.25;
		pts.push([cx + Math.cos(a) * rx * k, y]);
	}
	return closedSpline(pts);
};

/** Tapered stroke as a filled outline along a polyline (width w0 at start -> w1 at end), for fins, blades. */
export const taper = (pts: [number, number][], w0: number, w1: number): string => {
	const n = pts.length;
	const L: [number, number][] = [];
	const R: [number, number][] = [];
	for (let i = 0; i < n; i++) {
		const a = pts[Math.max(0, i - 1)];
		const b = pts[Math.min(n - 1, i + 1)];
		let nx = -(b[1] - a[1]);
		let ny = b[0] - a[0];
		const len = Math.hypot(nx, ny) || 1;
		nx /= len;
		ny /= len;
		const w = (w0 + (w1 - w0) * (i / (n - 1))) / 2;
		L.push([pts[i][0] + nx * w, pts[i][1] + ny * w]);
		R.push([pts[i][0] - nx * w, pts[i][1] - ny * w]);
	}
	return closedSpline([...L, ...R.reverse()], 0.9);
};
