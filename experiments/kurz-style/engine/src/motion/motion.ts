/**
 * Motion library (STYLE_BIBLE §9). Pure functions of time (seconds) so any frame renders on its own.
 *
 *   tokens     travel, drift, exit (beziers), settle / pop (springs), anticipate (dip-then-travel)
 *   springs    springAt(t, cfg) -> 0..1 with overshoot, any config; overshootPeak() for checks
 *   secondary  lagged(f, t, lag) follow-through, chain() sway with phase offset per segment, squash()
 *   ambient    breathe, bob, sway, blinkAt (seeded, never in sync), twinkle, pulse (lub-dub)
 *   camera     cameraAt(t, moves, drift) -> {x, y, zoom, roll}: eased moves + never-still drift + hand-held noise
 */
import {Easing, spring} from 'remotion';
import {fbm1, noise1, rand} from '../lib/rng';

export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const prog = (t: number, at: number, dur: number) => (dur <= 0 ? (t >= at ? 1 : 0) : clamp((t - at) / dur));

// ---------------------------------------------------------------- easing tokens (§9.2)

const travelE = Easing.bezier(0.16, 1, 0.3, 1);
const driftE = Easing.bezier(0.37, 0, 0.63, 1);
const exitE = Easing.bezier(0.7, 0, 0.84, 0);

export const ease = {
	/** object travel, pans, landings: fast out, long settle */
	travel: (x: number) => travelE(clamp(x)),
	/** camera drift ramps, ambient sways */
	drift: (x: number) => driftE(clamp(x)),
	/** exits: 60 % of the entrance duration */
	exit: (x: number) => exitE(clamp(x)),
	outQuad: (x: number) => 1 - (1 - clamp(x)) ** 2,
};

export type SpringCfg = {damping: number; stiffness: number; mass: number};
export const SETTLE: SpringCfg = {damping: 14, stiffness: 180, mass: 0.6};
export const POP: SpringCfg = {damping: 10, stiffness: 220, mass: 0.5};
export const SOFT: SpringCfg = {damping: 20, stiffness: 90, mass: 1};

/** spring progress 0 -> 1 (with overshoot) starting at `at` seconds */
export const springAt = (t: number, at: number, cfg: SpringCfg, fps = 30): number =>
	t < at ? 0 : spring({frame: (t - at) * fps, fps, config: cfg});

/** measured overshoot of a spring config (for the judge: settle ≤ 7 %, pop 10-25 %) */
export const overshootPeak = (cfg: SpringCfg, fps = 30): number => {
	let m = 0;
	for (let f = 0; f < fps * 3; f++) m = Math.max(m, spring({frame: f, fps, config: cfg}));
	return m - 1;
};

/**
 * Anticipation + travel + overshoot settle, as one 0..1 curve (value can dip below 0 and rise above 1):
 * a `dip` (6-10 %) opposite to the move over `antic` seconds, then a spring landing.
 */
export const anticipate = (t: number, at: number, o: {antic?: number; dip?: number; cfg?: SpringCfg; fps?: number} = {}): number => {
	const antic = o.antic ?? 0.17;
	const dip = o.dip ?? 0.08;
	if (t < at) return 0;
	if (t < at + antic) {
		const x = (t - at) / antic;
		return -dip * Math.sin((x * Math.PI) / 2) ** 2;
	}
	const s = springAt(t, at + antic, o.cfg ?? SETTLE, o.fps);
	return lerp(-dip, 1, s);
};

/** pop-in scale: 0 -> 1 with 10-25 % overshoot */
export const popIn = (t: number, at: number) => springAt(t, at, POP);

// ---------------------------------------------------------------- secondary motion (§9.7)

/** follow-through: sample the parent's motion `lag` seconds late (3-6 frames at 30 fps = 0.1-0.2 s) */
export const lagged = <T>(f: (t: number) => T, t: number, lag: number): T => f(t - lag);

/** chain sway: angle for segment i of n (tails, fins, kelp, tentacles): amplitude grows toward the tip */
export const chain = (t: number, i: number, n: number, o: {amp: number; freq: number; phase?: number; lagPerSeg?: number; seed?: string}) => {
	const s = (i + 1) / n;
	const ph = (o.phase ?? 0) - (o.lagPerSeg ?? 0.25) * i * 2 * Math.PI * 0.16;
	const wob = o.seed ? noise1(o.seed, t * 0.4 + i * 0.3) * 0.35 : 0;
	return o.amp * s * (Math.sin(2 * Math.PI * o.freq * t + ph) + wob);
};

/** volume-keeping squash & stretch from a velocity (px/frame) along y */
export const squash = (v: number, k = 0.01): {sx: number; sy: number} => {
	const sy = 1 + clamp(k * v, -0.12, 0.18);
	return {sx: 1 / Math.sqrt(sy), sy};
};

// ---------------------------------------------------------------- ambient layer (§9.3): always on

/** breathing scale: ±amp (1.5 %) with a 3-4 s period */
export const breathe = (t: number, seed: string, amp = 0.015, period = 3.5) =>
	1 + amp * Math.sin((2 * Math.PI * t) / period + rand(seed, 1) * 6.28);

/** slow float: px offset with a seeded phase */
export const bob = (t: number, seed: string, amp = 6, period = 4) => amp * Math.sin((2 * Math.PI * t) / period + rand(seed, 2) * 6.28);

/** noise sway in degrees (kelp, coral: 4-8 s periods) */
export const sway = (t: number, seed: string, amp = 3, period = 6) =>
	amp * (0.7 * Math.sin((2 * Math.PI * t) / period + rand(seed, 3) * 6.28) + 0.3 * fbm1(seed, t / period));

/**
 * Blink: 0 open .. 1 closed. Seeded intervals of 2-5 s, 0.18 s blinks, so two creatures never blink in sync.
 */
export const blinkAt = (t: number, seed: string): number => {
	let at = 0.4 + rand(seed, 0) * 2.2;
	for (let i = 1; i < 64 && at < t + 1; i++) {
		const d = t - at;
		if (d >= 0 && d < 0.18) return Math.sin((d / 0.18) * Math.PI);
		at += 2 + rand(seed, i) * 3;
	}
	return 0;
};

/** star / speck twinkle 0..1 at 0.2-0.6 Hz with random phase */
export const twinkle = (t: number, seed: string, i: number) => {
	const f = 0.2 + rand(seed, i * 3) * 0.4;
	return 0.5 + 0.5 * Math.sin(2 * Math.PI * f * t + rand(seed, i * 3 + 1) * 6.28);
};

/** living-light pulse (lub-dub), ±amp */
export const pulse = (t: number, period = 1.4, amp = 0.08) => {
	const x = (t % period) / period;
	const lub = Math.exp(-((x - 0.1) ** 2) / 0.002);
	const dub = 0.6 * Math.exp(-((x - 0.26) ** 2) / 0.002);
	return 1 + amp * (lub + dub - 0.3);
};

// ---------------------------------------------------------------- camera (§9.4)

export type Cam = {x: number; y: number; zoom: number; roll: number};
export type CamMove = {at: number; dur: number; to: Partial<Cam>; ease?: (x: number) => number};

/**
 * Camera at time t: start pose, eased moves (each with a lateral part so parallax shows), plus the
 * always-on drift (zoom %/s and lateral px/s) and hand-held noise (≤ 6 px, ≤ 0.5°). `steady` (0..1) fades the
 * hand-held noise out while a label is being read.
 */
export const cameraAt = (
	t: number,
	start: Cam,
	moves: CamMove[],
	drift: {zoomPerS?: number; xPerS?: number; yPerS?: number; hand?: number; seed?: string; steady?: number} = {},
): Cam => {
	const cam = {...start};
	for (const m of moves) {
		const e = (m.ease ?? ease.travel)(prog(t, m.at, m.dur));
		const from = {...cam};
		for (const key of Object.keys(m.to) as (keyof Cam)[]) cam[key] = lerp(from[key], m.to[key] as number, e);
	}
	cam.zoom *= 1 + (drift.zoomPerS ?? 0.008) * t;
	cam.x += (drift.xPerS ?? 8) * t;
	cam.y += (drift.yPerS ?? 0) * t;
	const h = (drift.hand ?? 4) * (1 - (drift.steady ?? 0));
	const s = drift.seed ?? 'cam';
	cam.x += h * fbm1(`${s}x`, t * 0.35);
	cam.y += h * fbm1(`${s}y`, t * 0.3);
	cam.roll += (h / 6) * 0.5 * fbm1(`${s}r`, t * 0.25);
	return cam;
};
