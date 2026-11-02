/**
 * Shared helpers for the explainer kit: prop readers, time tracks, easing,
 * path warping (for tail/fin idle animation) and smooth path builders.
 */
import {random} from 'remotion';

// ---------------------------------------------------------------- palette

import {FLAT} from './house/style';

// style A (house/style.ts): plates and the accent red come from the docs/HOUSE_STYLE.md palette
export const C = {
	oceanTop: '#1f6077',
	oceanMid: '#0d3344',
	oceanDeep: '#051720',
	abyss: '#02080c',
	ink: '#061017',
	panel: FLAT ? 'rgba(20, 9, 79, 0.9)' : 'rgba(4, 16, 23, 0.82)',
	panelLine: 'rgba(190, 230, 240, 0.16)',
	white: '#f3f6f7',
	muted: 'rgba(225, 238, 242, 0.62)',
	red: FLAT ? '#fa302a' : '#e5483d',
	redDeep: '#a32a22',
	yellow: '#f5c02e',
	green: '#4cd07d',
	cyan: '#6fd6e8',
	font: '"Montserrat", "Arial Black", "Helvetica Neue", Arial, sans-serif',
	condensed: '"Anton", "Arial Narrow", sans-serif',
};

// ---------------------------------------------------------------- prop readers

export const str = (v: unknown, d: string): string => (typeof v === 'string' ? v : d);
export const num = (v: unknown, d: number): number => (typeof v === 'number' && Number.isFinite(v) ? v : d);
export const bool = (v: unknown, d: boolean): boolean => (typeof v === 'boolean' ? v : d);
export const arr = <T = Record<string, unknown>>(v: unknown): T[] => (Array.isArray(v) ? (v as T[]) : []);
export const obj = (v: unknown): Record<string, unknown> =>
	v && typeof v === 'object' && !Array.isArray(v) ? (v as Record<string, unknown>) : {};

// ---------------------------------------------------------------- easing / time

export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const easeOut = (t: number) => 1 - Math.pow(1 - clamp(t), 3);
export const easeIn = (t: number) => Math.pow(clamp(t), 3);
export const easeInOut = (t: number) => {
	const x = clamp(t);
	return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
export const backOut = (t: number) => {
	const x = clamp(t);
	const c1 = 1.70158;
	const c3 = c1 + 1;
	return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
};
const EASES: Record<string, (t: number) => number> = {
	linear: (t) => clamp(t),
	in: easeIn,
	out: easeOut,
	inOut: easeInOut,
	backOut,
};

/** 0..1 progress of an animation that starts at `at` and lasts `dur` seconds. */
export const prog = (t: number, at: number, dur: number) => (dur <= 0 ? (t >= at ? 1 : 0) : clamp((t - at) / dur));

/**
 * A numeric prop that is either a constant or a keyframe track
 * [{t, v, ease?}] (scene-local seconds). Values are held before/after the ends.
 */
export function track(v: unknown, t: number, d: number): number {
	if (typeof v === 'number') return v;
	const kfs = arr<{t: number; v: number; ease?: string}>(v)
		.filter((k) => typeof k.t === 'number' && typeof k.v === 'number')
		.sort((a, b) => a.t - b.t);
	if (!kfs.length) return d;
	if (t <= kfs[0].t) return kfs[0].v;
	for (let i = 1; i < kfs.length; i++) {
		const k = kfs[i];
		if (t < k.t) {
			const p = kfs[i - 1];
			const e = EASES[k.ease ?? 'inOut'] ?? easeInOut;
			return lerp(p.v, k.v, e((t - p.t) / (k.t - p.t)));
		}
	}
	return kfs[kfs.length - 1].v;
}

export const rnd = (seed: string) => random(seed);

/** SVG-safe unique id prefix (React ids contain characters url(#...) dislikes). */
export const safeId = (id: string) => 'x' + id.replace(/[^a-zA-Z0-9_-]/g, '');

export const fmtNum = (n: number, decimals = 0) =>
	n.toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});

// ---------------------------------------------------------------- path warping

export type Pt = [number, number];
export type Warp = (x: number, y: number) => Pt;

const tokCache = new Map<string, (string | number)[]>();
function tokens(d: string): (string | number)[] {
	let t = tokCache.get(d);
	if (!t) {
		t = (d.match(/[MLCQZ]|-?(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?/g) ?? []).map((s) =>
			/[MLCQZ]/.test(s) ? s : parseFloat(s),
		);
		tokCache.set(d, t);
	}
	return t;
}

/**
 * Apply a point warp to an absolute path (only M L C Q Z commands).
 * Every coordinate pair, control points included, goes through `f`, so a body and the
 * details drawn on it bend together.
 */
export function warp(d: string, f?: Warp): string {
	if (!f) return d;
	const tk = tokens(d);
	let out = '';
	for (let i = 0; i < tk.length; ) {
		const c = tk[i];
		if (typeof c === 'string') {
			out += c;
			i++;
		} else {
			const [x, y] = f(c, tk[i + 1] as number);
			out += ` ${x.toFixed(1)} ${y.toFixed(1)} `;
			i += 2;
		}
	}
	return out;
}

/**
 * Travelling-wave body bend. `head` and `tail` are x positions in the drawing; points
 * near the head stay still, the tail swings by `amp` (vertical displacement).
 */
export function swimWarp(o: {head: number; tail: number; amp: number; t: number; freq: number; k?: number; pow?: number; phase?: number}): Warp {
	const k = o.k ?? 2.4;
	const pow = o.pow ?? 2;
	const span = o.head - o.tail;
	const w = Math.PI * 2 * o.freq;
	return (x, y) => {
		const u = clamp((o.head - x) / span);
		return [x, y + o.amp * Math.pow(u, pow) * Math.sin(w * o.t + (o.phase ?? 0) - u * k)];
	};
}

export const compose =
	(...fs: (Warp | undefined)[]): Warp =>
	(x, y) => {
		let p: Pt = [x, y];
		for (const f of fs) if (f) p = f(p[0], p[1]);
		return p;
	};

// ---------------------------------------------------------------- smooth shapes

const f1 = (n: number) => n.toFixed(1);

/** Catmull-Rom spline through points, as absolute cubic Beziers. */
export function smooth(pts: Pt[], closed = false, tension = 1): string {
	const n = pts.length;
	if (n < 2) return '';
	const P = (i: number) => (closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))]);
	let d = `M ${f1(pts[0][0])} ${f1(pts[0][1])}`;
	const segs = closed ? n : n - 1;
	for (let i = 0; i < segs; i++) {
		const p0 = P(i - 1);
		const p1 = P(i);
		const p2 = P(i + 1);
		const p3 = P(i + 2);
		const c1: Pt = [p1[0] + ((p2[0] - p0[0]) / 6) * tension, p1[1] + ((p2[1] - p0[1]) / 6) * tension];
		const c2: Pt = [p2[0] - ((p3[0] - p1[0]) / 6) * tension, p2[1] - ((p3[1] - p1[1]) / 6) * tension];
		d += ` C ${f1(c1[0])} ${f1(c1[1])} ${f1(c2[0])} ${f1(c2[1])} ${f1(p2[0])} ${f1(p2[1])}`;
	}
	return closed ? d + ' Z' : d;
}

/** A tapered ribbon (tentacle, arm, tail) around a centre line; widths per point. */
export function ribbon(center: Pt[], widths: number[]): string {
	const L: Pt[] = [];
	const R: Pt[] = [];
	for (let i = 0; i < center.length; i++) {
		const a = center[Math.max(0, i - 1)];
		const b = center[Math.min(center.length - 1, i + 1)];
		let nx = -(b[1] - a[1]);
		let ny = b[0] - a[0];
		const len = Math.hypot(nx, ny) || 1;
		nx /= len;
		ny /= len;
		const w = widths[i] / 2;
		L.push([center[i][0] + nx * w, center[i][1] + ny * w]);
		R.push([center[i][0] - nx * w, center[i][1] - ny * w]);
	}
	return smooth([...L, ...R.reverse()], true, 0.9);
}

/** Centre line from a start point, initial angle (deg) and per-step bend function. */
export function curl(start: Pt, angleDeg: number, length: number, steps: number, bend: (s: number) => number): Pt[] {
	const pts: Pt[] = [start];
	let a = (angleDeg * Math.PI) / 180;
	let [x, y] = start;
	const ds = length / steps;
	for (let i = 1; i <= steps; i++) {
		const s = i / steps;
		a += (bend(s) * Math.PI) / 180;
		x += Math.cos(a) * ds;
		y += Math.sin(a) * ds;
		pts.push([x, y]);
	}
	return pts;
}

export const pathOfPoints = (pts: Pt[], closed = true) =>
	'M ' + pts.map((p) => `${f1(p[0])} ${f1(p[1])}`).join(' L ') + (closed ? ' Z' : '');
