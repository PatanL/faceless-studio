// Small animation toolkit for the TIS remake: easings, keyframes, noise, camera, lip-sync.
import {WORDS} from '../data/words';

export const FPS = 30;
export type Ease = (t: number) => number;

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export const E = {
	linear: (t: number) => t,
	inQuad: (t: number) => t * t,
	outQuad: (t: number) => 1 - (1 - t) * (1 - t),
	inCubic: (t: number) => t * t * t,
	outCubic: (t: number) => 1 - Math.pow(1 - t, 3),
	inOutCubic: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
	inOutQuint: (t: number) => (t < 0.5 ? 16 * t ** 5 : 1 - Math.pow(-2 * t + 2, 5) / 2),
	inOutSine: (t: number) => -(Math.cos(Math.PI * t) - 1) / 2,
	outExpo: (t: number) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t)),
	inExpo: (t: number) => (t <= 0 ? 0 : Math.pow(2, 10 * t - 10)),
	outBack: (t: number) => {
		const c1 = 1.9;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	},
};

/** 0..1 progress of t through [t0,t1] with easing. */
export const seg = (t: number, t0: number, t1: number, ease: Ease = E.inOutCubic) =>
	ease(clamp((t - t0) / (t1 - t0)));

/** Piecewise keyframes: [time, value, easeIntoThisKey?]. Holds outside the range. */
export function kf(t: number, keys: [number, number, Ease?][]): number {
	if (t <= keys[0][0]) return keys[0][1];
	for (let i = 1; i < keys.length; i++) {
		const [t1, v1, e] = keys[i];
		const [t0, v0] = keys[i - 1];
		if (t <= t1) return lerp(v0, v1, (e ?? E.inOutCubic)(clamp((t - t0) / (t1 - t0 || 1))));
	}
	return keys[keys.length - 1][1];
}

export const osc = (t: number, hz: number, phase = 0) => Math.sin(2 * Math.PI * (hz * t + phase));

export function hash(n: number): number {
	const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
	return s - Math.floor(s);
}

/** Smooth 1D value noise in [-1,1]. */
export function noise(x: number, seed = 0): number {
	const i = Math.floor(x);
	const f = x - i;
	const u = f * f * (3 - 2 * f);
	return lerp(hash(i + seed * 57.3), hash(i + 1 + seed * 57.3), u) * 2 - 1;
}

/** Seeded RNG for authoring deterministic decoration. */
export function rng(seed: number) {
	let s = seed * 9301 + 49297;
	return () => {
		s = (s * 9301 + 49297) % 233280;
		return s / 233280;
	};
}

// ---------------------------------------------------------------- camera
export type Cam = {x: number; y: number; s: number; r: number};
export const CAM0: Cam = {x: 540, y: 960, s: 1, r: 0};

/** Camera that puts world point w at screen point p with scale s and rotation r (deg). */
export function look(w: [number, number], p: [number, number], s: number, r: number): Cam {
	const dx = (p[0] - 540) / s;
	const dy = (p[1] - 960) / s;
	const a = (-r * Math.PI) / 180;
	const rx = dx * Math.cos(a) - dy * Math.sin(a);
	const ry = dx * Math.sin(a) + dy * Math.cos(a);
	return {x: w[0] - rx, y: w[1] - ry, s, r};
}

export function camLerp(a: Cam, b: Cam, u: number): Cam {
	return {
		x: lerp(a.x, b.x, u),
		y: lerp(a.y, b.y, u),
		s: Math.exp(lerp(Math.log(a.s), Math.log(b.s), u)),
		r: lerp(a.r, b.r, u),
	};
}

/** Camera keyframes; the ease is used for the segment that ends at that key. */
export function camAt(t: number, keys: [number, Cam, Ease?][]): Cam {
	if (t <= keys[0][0]) return keys[0][1];
	for (let i = 1; i < keys.length; i++) {
		const [t1, c1, e] = keys[i];
		const [t0, c0] = keys[i - 1];
		if (t <= t1) return camLerp(c0, c1, (e ?? E.inOutCubic)(clamp((t - t0) / (t1 - t0 || 1))));
	}
	return keys[keys.length - 1][1];
}

export const camT = (c: Cam) =>
	`translate(540 960) rotate(${c.r.toFixed(3)}) scale(${c.s.toFixed(4)}) translate(${(-c.x).toFixed(2)} ${(-c.y).toFixed(2)})`;

/** Parallax copy of a camera for a layer at depth factor p (1 = same plane). */
export const para = (c: Cam, p: number, ax: number, ay: number): Cam => ({
	...c,
	x: ax + (c.x - ax) * p,
	y: ay + (c.y - ay) * p,
});

// ---------------------------------------------------------------- lip-sync, blinks
export function wordAt(t: number): number {
	for (let i = 0; i < WORDS.length; i++) {
		const [s, e] = WORDS[i];
		if (t >= s - 0.03 && t <= e + 0.02) return i;
		if (s > t) break;
	}
	return -1;
}

export type Mouth = 'closed' | 'open' | 'mid' | 'O' | 'grin' | 'yell' | 'smile' | 'o' | 'flat';

/** Mouth shape for a talking character at time t (~7 Hz alternation while a word is spoken). */
export function talkMouth(t: number, seed = 0, rest: Mouth = 'closed'): Mouth {
	const w = wordAt(t);
	if (w < 0) return rest;
	const k = Math.floor(t * 7.5 + seed * 3.1);
	const cycle: Mouth[] = ['open', 'mid', 'O', 'open', 'closed', 'mid', 'grin', 'open'];
	return cycle[(k + w) % cycle.length];
}

export const isTalking = (t: number) => wordAt(t) >= 0;

/** true while eyes are shut (4 frames every ~2.6-4.2 s, seeded). */
export function blinking(t: number, seed = 0): boolean {
	const period = 2.6 + hash(seed) * 1.6;
	const ph = (t + hash(seed + 3) * period) % period;
	return ph < 4 / FPS;
}
