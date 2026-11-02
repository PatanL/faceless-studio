import {Easing, random, spring} from 'remotion';
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
	/** extra per-axis scale (squash & stretch); 1 = none */
	sx?: number;
	sy?: number;
	/** squash pivot as a fraction of the layer height (1 = bottom edge stays put) */
	pivotY?: number;
};

const NEUTRAL: AnimState = {dx: 0, dy: 0, scale: 1, opacity: 1};

// house-style springs (STYLE_BIBLE §9.2): pop = 10-25 % overshoot, landing = a settle with one small overshoot
const POP_SPRING = {damping: 10, stiffness: 220, mass: 0.5};
const LAND_SPRING = {damping: 11, stiffness: 180, mass: 0.6};
/** narrowest a popping layer may draw, as a fraction of its rest width (the YOU-pop fix: no pencil-thin frames) */
export const POP_MIN_WIDTH = 0.6;

/**
 * popSpring scale at `ts` seconds after the pop starts: both axes together (never one axis leading the other), floored
 * at POP_MIN_WIDTH so the first visible frame is already a recognisable shape, then a spring with overshoot.
 */
export function popSpringScale(ts: number): number {
	if (ts <= 0) return POP_MIN_WIDTH;
	return Math.max(POP_MIN_WIDTH, spring({frame: ts * 30, fps: 30, config: POP_SPRING}));
}

/** dropSquash state at `ts` seconds after release: gravity fall over `fall` s, stretch, then a landing squash. */
export function dropSquashAt(ts: number, distance: number, fall = 0.22, squash = 0.2): {dy: number; sx: number; sy: number} {
	if (ts < fall) {
		const u = Math.max(0, ts) / fall;
		const sy = 1 + Math.min(0.12, 0.12 * u); // stretch along the fall
		return {dy: -distance * (1 - u * u), sx: 1 / Math.sqrt(sy), sy};
	}
	const s = spring({frame: (ts - fall) * 30, fps: 30, config: LAND_SPRING});
	const sy = 1 - squash * (1 - s);
	return {dy: 0, sx: 1 / Math.sqrt(Math.max(0.5, sy)), sy};
}

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
		case 'popSpring': {
			const ts = p * a.duration;
			const k = popSpringScale(ts);
			return {...NEUTRAL, opacity: p <= 0 ? 0 : clamp01(ts / 0.1), sx: k, sy: k};
		}
		case 'dropSquash': {
			const ts = p * a.duration;
			const fall = Math.min(0.22, a.duration * 0.4);
			const st = dropSquashAt(ts, d, fall);
			return {...NEUTRAL, opacity: p <= 0 ? 0 : clamp01(ts / 0.066), dy: st.dy, sx: st.sx, sy: st.sy, pivotY: 1};
		}
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
				sx: (s.sx ?? 1) * (x.sx ?? 1),
				sy: (s.sy ?? 1) * (x.sy ?? 1),
				pivotY: x.pivotY ?? s.pivotY,
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
