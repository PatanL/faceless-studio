import type React from 'react';
/**
 * Shared helpers for the stick kit (round-head story characters, house style A tokens).
 * Flat shapes: one solid colour per shape, one flat shadow shape per object, no gradients.
 *
 * Storybook look (story lane v5, research/references/STORY_LANE_TUTORIAL_CHECK.md gap 3): every token goes through
 * `storybook()`, an OKLab remap toward the RicksClips3000 grade (HSV S median 0.41-0.61, colourfulness 23-34, mid-tones
 * not dark, violet-blue shadows with chroma <= ~35, mildly warm highlights): darks are lifted toward the mid-tones,
 * chroma is cut hardest in the darks, light tones get a touch of warmth. Ink lines (`INK`, `inkG`) skip the remap so
 * they stay dark: components take an `ink` prop (stroke width in their own viewBox units) that outlines every filled
 * shape (the reference has ink on ~55-65 % of strong edges; v4 had 17 %).
 */
import {c as houseC, hexToLab, labToHex} from '../house/color';
import {arr, clamp} from '../util';

const SB = new Map<string, string>();
export function storybook(hex: string): string {
	const hit = SB.get(hex);
	if (hit) return hit;
	const [L0, A0, B0] = hexToLab(hex);
	const lift = 0.24 * clamp((L0 - 0.24) / 0.22); // mid-tones up, the deepest shades stay deep (non-ink p5 <= ~0.23)
	const L = L0 < 0.66 ? L0 + (0.66 - L0) * lift : L0;
	const k = L < 0.45 ? 0.42 : L > 0.8 ? 0.66 : 0.42 + ((L - 0.45) / 0.35) * 0.24;
	let A = A0 * k;
	let B = B0 * k;
	if (L > 0.82) {
		A += 0.004;
		B += 0.014 * (L - 0.82) / 0.18;
	}
	const out = labToHex([L, A, B]);
	SB.set(hex, out);
	return out;
}

/** palette token or #hex -> the stick kit's storybook colour */
export const c = (tok: string): string => storybook(houseC(tok));
/** ink for outlines and stick limbs: deep violet, outside the remap so lines stay dark (Y' ~0.07) */
export const INK = '#1b1240';
/** SVG group attributes that ink-outline every filled child shape that has no stroke of its own */
export const inkG = (w: unknown): React.SVGProps<SVGGElement> =>
	typeof w === 'number' && w > 0 ? {stroke: INK, strokeWidth: w, strokeLinejoin: 'round', strokeLinecap: 'round'} : {};

export const K = {
	ink: INK, // limbs, eyes, mouths (deep violet ink, never black)
	inkDeep: INK,
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
