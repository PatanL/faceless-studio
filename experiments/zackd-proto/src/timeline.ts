// Timeline for the 12.9 s freezer beat. Every value is a pure function of t (seconds), so any frame renders alone.
// Word times come from Kokoro (public/audio/captions.json); the beats below are pinned to those words.

export const FPS = 30;
export const DURATION_S = 12.9;
export const DURATION_FRAMES = Math.round(DURATION_S * FPS);

export type V3 = [number, number, number];

export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const lerp3 = (a: V3, b: V3, k: number): V3 => [lerp(a[0], b[0], k), lerp(a[1], b[1], k), lerp(a[2], b[2], k)];
export const ramp = (t: number, t0: number, t1: number) => clamp((t - t0) / (t1 - t0));
export const easeInOut = (x: number) => {
	x = clamp(x);
	return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
};
export const easeOut = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
export const easeIn = (x: number) => Math.pow(clamp(x), 3);
/** 0 -> 1 between t0..t1, holds, 1 -> 0 between t2..t3 */
export const window4 = (t: number, t0: number, t1: number, t2: number, t3: number) =>
	Math.min(easeInOut(ramp(t, t0, t1)), 1 - easeInOut(ramp(t, t2, t3)));

// ---- key word times (s), from captions.json ----
export const W = {
	locked: 0.93,
	freezer: 2.38,
	dont: 3.35,
	heat: 4.5,
	pounding: 4.8,
	door: 5.93,
	because: 6.84,
	latch: 8.25,
	is: 8.73,
	glow: 9.0,
	knob: 9.93,
	pushes: 10.55,
	open: 11.06,
	inside: 11.68,
	lastWordEnd: 12.31,
};
export const KNOCKS = [4.8, 5.12, 5.44]; // knock3 SFX hits at +0, +0.32, +0.64 s
export const SLAM = 0.38;

// ---- shots: camera from -> to with ease-in-out push; cut type on entry ----
export type Shot = {
	id: string;
	t0: number;
	t1: number;
	pos: [V3, V3];
	target: [V3, V3];
	fov: [number, number];
	enter: 'cut' | 'whip';
	showChar: boolean;
	showArm?: boolean;
	handheld?: number; // drift amplitude (m)
};

// frame 0 composition == last frame composition (loop seam)
const WIDE_POS: V3 = [0.95, 1.28, 1.55];
const WIDE_TGT: V3 = [0.2, 0.98, -1.7];

export const SHOTS: Shot[] = [
	// 1. door already slamming shut on frame 0, "If you ever get locked"
	{id: 'slam', t0: 0, t1: 1.36, pos: [WIDE_POS, [0.85, 1.3, 1.15]], target: [WIDE_TGT, [0.25, 1.02, -1.7]], fov: [60, 58], enter: 'cut', showChar: true},
	// 2. low-angle wide of the freezer, "inside a walk-in"
	{id: 'room', t0: 1.36, t1: 2.38, pos: [[0.82, 0.3, 1.35], [0.72, 0.34, 1.0]], target: [[-0.4, 1.7, -1.2], [-0.25, 1.75, -1.5]], fov: [72, 70], enter: 'whip', showChar: true},
	// 3. face close-up, frost and breath, "freezer"
	{id: 'face', t0: 2.38, t1: 3.35, pos: [[0.55, 1.58, 0.45], [0.47, 1.55, 0.22]], target: [[0.3, 1.47, -0.8], [0.3, 1.49, -0.8]], fov: [40, 38], enter: 'cut', showChar: true},
	// 4. mid shot with heat aura draining, "don't burn your body heat"
	{id: 'heat', t0: 3.35, t1: 4.8, pos: [[0.3, 1.0, 1.6], [0.3, 1.05, 1.15]], target: [[0.3, 1.12, -0.8], [0.3, 1.15, -0.8]], fov: [48, 46], enter: 'whip', showChar: true},
	// 5. over the shoulder, fists on the door, "pounding on the steel door"
	{id: 'pound', t0: 4.8, t1: 6.84, pos: [[-0.55, 1.62, -0.25], [-0.45, 1.55, -0.5]], target: [[0.35, 1.3, -2.0], [0.35, 1.3, -2.0]], fov: [55, 52], enter: 'cut', showChar: true, handheld: 0.012},
	// 6. whip to the latch, "because right beside the latch"
	{id: 'latch', t0: 6.84, t1: 8.73, pos: [[0.05, 1.3, -0.75], [0.2, 1.2, -1.0]], target: [[0.6, 1.03, -1.95], [0.6, 1.03, -1.95]], fov: [42, 40], enter: 'whip', showChar: false},
	// 7. money shot: the knob glows, the hand presses it, "is a glow-in-the-dark knob that pushes it"
	{id: 'knob', t0: 8.73, t1: 11.06, pos: [[1.1, 1.22, -1.05], [0.98, 1.13, -1.3]], target: [[0.5, 1.02, -1.86], [0.5, 1.02, -1.86]], fov: [38, 35], enter: 'cut', showChar: false, showArm: true},
	// 8. back to the frame-0 wide as the door swings open, "open from inside" + tail
	{id: 'open', t0: 11.06, t1: DURATION_S + 0.001, pos: [[0.75, 1.32, 0.8], WIDE_POS], target: [[0.25, 1.05, -1.7], WIDE_TGT], fov: [56, 60], enter: 'cut', showChar: true},
];

export const shotAt = (t: number) => SHOTS.find((s) => t >= s.t0 && t < s.t1) ?? SHOTS[SHOTS.length - 1];

export function cameraAt(t: number) {
	const s = shotAt(t);
	const k = easeInOut((t - s.t0) / (s.t1 - s.t0));
	const pos = lerp3(s.pos[0], s.pos[1], k);
	const target = lerp3(s.target[0], s.target[1], k);
	if (s.handheld) {
		const a = s.handheld;
		pos[0] += a * Math.sin(t * 2.1 + 0.3) + a * 0.5 * Math.sin(t * 5.3);
		pos[1] += a * 0.7 * Math.sin(t * 1.7 + 1.1);
	}
	return {pos, target, fov: lerp(s.fov[0], s.fov[1], k), shot: s};
}

/** whip smear strength 0..1 around whip cuts (3 frames either side) */
export function whipAt(t: number) {
	let best = 0;
	let dir = 1;
	for (const s of SHOTS) {
		if (s.enter !== 'whip') continue;
		const d = (t - s.t0) / (3 / FPS);
		if (Math.abs(d) < 1) {
			const v = 1 - Math.abs(d);
			if (v > best) {
				best = v;
				dir = d < 0 ? 1 : -1; // outgoing frames slide left, incoming arrive from the right
			}
		}
	}
	return {amount: best, dir};
}

/** screen shake (fraction of frame) after impacts */
export function shakeAt(t: number) {
	let x = 0;
	let y = 0;
	for (const ti of [SLAM, ...KNOCKS]) {
		const a = t - ti;
		if (a < 0 || a > 0.35) continue;
		const env = Math.exp(-a / 0.1);
		x += 0.016 * env * Math.sin(2 * Math.PI * 5 * a + 0.4);
		y += 0.012 * env * Math.sin(2 * Math.PI * 6 * a);
	}
	return {x, y};
}

// ---- world state ----
export const DOOR_OPEN = 0.95; // rad
export function doorAngle(t: number) {
	if (t < W.open) return DOOR_OPEN * (1 - easeIn(ramp(t, 0, SLAM)));
	return DOOR_OPEN * easeOut(ramp(t, W.open, W.open + 0.95));
}
export const outsideLight = (t: number) => clamp(doorAngle(t) / 0.35);
/** room light level: dims for the glow-in-the-dark reveal, back up as the door opens */
export const roomLight = (t: number) => 1 - 0.62 * window4(t, W.glow - 0.05, W.glow + 0.3, W.open - 0.1, W.open + 0.5);
export const knobGlow = (t: number) => window4(t, W.glow - 0.05, W.glow + 0.15, W.inside, W.lastWordEnd + 0.3);
export const latchHighlight = (t: number) => window4(t, W.latch - 0.05, W.latch + 0.05, W.is + 0.1, W.is + 0.3);
export const knobPush = (t: number) => easeOut(ramp(t, W.pushes - 0.05, W.pushes + 0.15)) * (1 - easeInOut(ramp(t, W.open + 0.3, W.open + 0.7)));
/** body heat 1 -> drains while talking about it, drops on each knock */
export function heat(t: number) {
	let h = 1 - 0.35 * easeInOut(ramp(t, W.dont, W.pounding));
	for (const k of KNOCKS) h -= 0.12 * easeOut(ramp(t, k, k + 0.15));
	return clamp(h);
}
export const auraVisible = (t: number) => t >= W.dont - 0.05 && t < W.because;
/** failure flush: whole frame toward red on "door" */
export const failure = (t: number) => window4(t, W.door - 0.02, W.door + 0.15, W.because - 0.35, W.because - 0.05);
