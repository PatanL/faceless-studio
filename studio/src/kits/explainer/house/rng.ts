/**
 * Seeded randomness and smooth noise. Everything is a pure function of (seed, t), because Remotion renders
 * frames out of order on several tabs: nothing may depend on the previous frame.
 */

/** string|number seed -> 32-bit int */
export const hashSeed = (s: string | number): number => {
	const str = String(s);
	let h = 2166136261;
	for (let i = 0; i < str.length; i++) {
		h ^= str.charCodeAt(i);
		h = Math.imul(h, 16777619);
	}
	return h >>> 0;
};

/** mulberry32: returns a generator of floats in [0, 1). */
export const rng = (seed: string | number) => {
	let a = hashSeed(seed);
	return () => {
		a |= 0;
		a = (a + 0x6d2b79f5) | 0;
		let t = Math.imul(a ^ (a >>> 15), 1 | a);
		t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
		return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
	};
};

/** deterministic float in [0,1) for (seed, i) */
export const rand = (seed: string | number, i: number): number => {
	const r = rng(`${seed}:${i}`);
	return r();
};

const lattice = (seed: number, i: number) => {
	let h = (seed ^ Math.imul(i, 374761393)) >>> 0;
	h = Math.imul(h ^ (h >>> 13), 1274126177);
	h ^= h >>> 16;
	return ((h >>> 0) / 4294967296) * 2 - 1;
};

/** smooth 1D value noise in [-1, 1] (quintic fade), unit frequency */
export const noise1 = (seed: string | number, x: number): number => {
	const s = hashSeed(seed);
	const i = Math.floor(x);
	const f = x - i;
	const u = f * f * f * (f * (f * 6 - 15) + 10);
	return lattice(s, i) * (1 - u) + lattice(s, i + 1) * u;
};

/** 2-octave fractal noise in about [-1, 1] */
export const fbm1 = (seed: string | number, x: number): number =>
	(noise1(seed, x) * 0.67 + noise1(`${seed}~`, x * 2.03 + 17.1) * 0.33);
