import {Easing, random} from 'remotion';
import type {Anim, Coord, EaseName, Idle, Keyframe} from './schema';

export const clamp01 = (v: number) => Math.max(0, Math.min(1, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

const EASES: Record<EaseName, (t: number) => number> = {
	linear: (t) => t,
	in: Easing.in(Easing.cubic),
	out: Easing.out(Easing.cubic),
	inOut: Easing.inOut(Easing.cubic),
	backIn: Easing.in(Easing.back(1.7)),
	backOut: Easing.out(Easing.back(1.7)),
	elastic: Easing.out(Easing.elastic(1)),
	bounce: Easing.bounce,
	step: (t) => (t >= 1 ? 1 : 0),
};
export const ease = (name: EaseName | undefined, t: number) => EASES[name ?? 'inOut'](clamp01(t));

/** Resolve "50%" / 120 to pixels against a reference length. */
export const px = (c: Coord | undefined, ref: number, fallback = 0): number => {
	if (c === undefined) return fallback;
	if (typeof c === 'number') return c;
	return (parseFloat(c) / 100) * ref;
};

type NumKey = 'x' | 'y' | 'scale' | 'scaleX' | 'scaleY' | 'rotate' | 'opacity' | 'zoom';

/**
 * Sample one property from a keyframe list at time t (seconds).
 * Only keyframes that define the property count. Before the first / after the last
 * keyframe the value is held. With no keyframes for the property, `base` is returned.
 */
export function sample<K extends {t: number; ease?: EaseName}>(
	kfs: K[],
	prop: NumKey,
	t: number,
	base: number,
	resolve: (v: unknown) => number = (v) => v as number,
): number {
	let prev: K | null = null;
	for (const k of kfs) {
		const v = (k as Record<string, unknown>)[prop];
		if (v === undefined) continue;
		if (k.t <= t) {
			prev = k;
			continue;
		}
		if (!prev) return resolve(v);
		const span = k.t - prev.t;
		const p = span <= 0 ? 1 : (t - prev.t) / span;
		return lerp(resolve((prev as Record<string, unknown>)[prop]), resolve(v), ease(k.ease, p));
	}
	if (prev) return resolve((prev as Record<string, unknown>)[prop]);
	return base;
}

export const sortByT = <T extends {t: number}>(a: T[]) => [...a].sort((p, q) => p.t - q.t);

export type AnimState = {
	dx: number;
	dy: number;
	scale: number;
	opacity: number;
	clip?: string;
};

const NEUTRAL: AnimState = {dx: 0, dy: 0, scale: 1, opacity: 1};

/** p = 0 means hidden, 1 means fully shown. */
function animAt(a: Anim, p: number): AnimState {
	const e = ease('out', p);
	const d = a.distance;
	switch (a.type) {
		case 'fade':
			return {...NEUTRAL, opacity: e};
		case 'pop':
			return {...NEUTRAL, opacity: clamp01(p * 3), scale: ease('backOut', p) * 1 + 0.0001};
		case 'slideUp':
			return {...NEUTRAL, opacity: clamp01(p * 2), dy: (1 - e) * d};
		case 'slideDown':
			return {...NEUTRAL, opacity: clamp01(p * 2), dy: -(1 - e) * d};
		case 'slideLeft':
			return {...NEUTRAL, opacity: clamp01(p * 2), dx: (1 - e) * d};
		case 'slideRight':
			return {...NEUTRAL, opacity: clamp01(p * 2), dx: -(1 - e) * d};
		case 'zoomIn':
			return {...NEUTRAL, opacity: e, scale: lerp(0.6, 1, e)};
		case 'zoomOut':
			return {...NEUTRAL, opacity: e, scale: lerp(1.5, 1, e)};
		case 'wipeRight':
			return {...NEUTRAL, clip: `inset(0 ${(1 - e) * 100}% 0 0)`};
		case 'wipeDown':
			return {...NEUTRAL, clip: `inset(0 0 ${(1 - e) * 100}% 0)`};
		case 'drop':
			return {...NEUTRAL, opacity: clamp01(p * 4), dy: -(1 - ease('bounce', p)) * d};
	}
}

/** Combined enter/exit state for a layer at scene-local time t. */
export function enterExit(
	t: number,
	enter: Anim | undefined,
	exit: Anim | undefined,
	start: number,
	end: number,
): AnimState {
	let s = NEUTRAL;
	if (enter) {
		const at = enter.at ?? start;
		s = animAt(enter, (t - at) / enter.duration);
	}
	if (exit) {
		const at = exit.at ?? end - exit.duration;
		if (t >= at) {
			const x = animAt(exit, 1 - (t - at) / exit.duration);
			s = {
				dx: s.dx + x.dx,
				dy: s.dy + x.dy,
				scale: s.scale * x.scale,
				opacity: s.opacity * x.opacity,
				clip: x.clip ?? s.clip,
			};
		}
	}
	return s;
}

export type IdleState = {dx: number; dy: number; rotate: number; sx: number; sy: number};

export function idleAt(idles: Idle[], t: number, seed: string): IdleState {
	const st: IdleState = {dx: 0, dy: 0, rotate: 0, sx: 1, sy: 1};
	idles.forEach((i, n) => {
		const w = 2 * Math.PI * i.speed * t + i.phase;
		switch (i.type) {
			case 'bob':
				st.dy += Math.sin(w) * (i.amount ?? 12);
				break;
			case 'float':
				st.dx += Math.sin(w * 0.7) * (i.amount ?? 14);
				st.dy += Math.cos(w) * (i.amount ?? 14);
				break;
			case 'breathe':
				st.sy *= 1 + Math.sin(w) * (i.amount ?? 0.02);
				st.sx *= 1 - Math.sin(w) * (i.amount ?? 0.02) * 0.4;
				break;
			case 'pulse': {
				const k = 1 + Math.abs(Math.sin(w)) * (i.amount ?? 0.06);
				st.sx *= k;
				st.sy *= k;
				break;
			}
			case 'sway':
				st.rotate += Math.sin(w) * (i.amount ?? 3);
				break;
			case 'spin':
				st.rotate += 360 * i.speed * t;
				break;
			case 'jitter': {
				const step = Math.floor(t * 24 * Math.max(0.1, i.speed));
				const a = i.amount ?? 4;
				st.dx += (random(`${seed}-jx-${n}-${step}`) - 0.5) * 2 * a;
				st.dy += (random(`${seed}-jy-${n}-${step}`) - 0.5) * 2 * a;
				break;
			}
		}
	});
	return st;
}

/** Smooth deterministic noise in [-1, 1] from a sum of sines with seeded phases. */
export function noise1(seed: string, t: number, freq: number): number {
	let v = 0;
	const mults = [1, 1.93, 3.71];
	mults.forEach((m, i) => {
		const ph = random(`${seed}-${i}`) * Math.PI * 2;
		v += Math.sin(t * freq * m * Math.PI * 2 + ph) / (i + 1);
	});
	return v / 1.83;
}

export type KF = Keyframe;
