/**
 * Shared helpers for the stick kit (round-head story characters in house style A colours).
 * Flat shapes only: one solid colour per shape, one flat shadow shape per object, no outlines, no gradients.
 */
import {c} from '../house/color';
import {arr, clamp} from '../util';

export {c};
export const K = {
	ink: c('ink-1'), // limbs, eyes, mouths (indigo, never black)
	inkDeep: c('ink-0'),
	skin: c('bone-1'),
	skinShade: c('bone-0'),
	cheek: c('magenta-4'),
	gold: c('amber-4'),
	goldShade: c('amber-2'),
	wood: c('ochre-1'),
	woodShade: c('ochre-0'),
	woodLight: c('ochre-2'),
	red: c('coral-2'),
};

/** A discrete prop that changes over time: a constant, or [{t, v}] (held from each t). */
export function step<T>(v: unknown, t: number, d: T): T {
	if (v === undefined || v === null) return d;
	if (!Array.isArray(v)) return v as T;
	const ks = arr<{t: number; v: T}>(v).filter((k) => typeof k.t === 'number').sort((a, b) => a.t - b.t);
	let out = d;
	for (const k of ks) if (t >= k.t) out = k.v;
	if (ks.length && t < ks[0].t) out = ks[0].v;
	return out;
}

/** the previous and current value of a discrete track plus seconds since the switch (for blending poses) */
export function stepBlend<T>(v: unknown, t: number, d: T): {prev: T; cur: T; since: number} {
	if (!Array.isArray(v)) return {prev: (v as T) ?? d, cur: (v as T) ?? d, since: 99};
	const ks = arr<{t: number; v: T}>(v).filter((k) => typeof k.t === 'number').sort((a, b) => a.t - b.t);
	if (!ks.length) return {prev: d, cur: d, since: 99};
	let i = -1;
	for (let j = 0; j < ks.length; j++) if (t >= ks[j].t) i = j;
	if (i < 0) return {prev: ks[0].v, cur: ks[0].v, since: 99};
	return {prev: i > 0 ? ks[i - 1].v : ks[i].v, cur: ks[i].v, since: t - ks[i].t};
}

/** is t inside any [a, b] window */
export const inWin = (wins: unknown, t: number): boolean =>
	arr<number[]>(wins).some((w) => Array.isArray(w) && t >= w[0] && t <= w[1]);

export const smoothstep = (t: number) => {
	const x = clamp(t);
	return x * x * (3 - 2 * x);
};

/** deterministic hash noise 0..1 */
export const hash = (n: number) => {
	const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
	return s - Math.floor(s);
};

export const f = (n: number) => n.toFixed(1);
