import {noise1, px, sample, sortByT, clamp01} from './anim';
import type {Camera} from './schema';

export type CamState = {x: number; y: number; zoom: number; rotate: number};
export type ShakeState = {dx: number; dy: number; rotate: number};

/** Expand a camera preset into keyframes spanning the scene. */
function presetKeyframes(cam: Camera, W: number, H: number, dur: number) {
	const a = cam.amount;
	const cx = W / 2;
	const cy = H / 2;
	const pan = Math.min(W, H) * 0.12 * a;
	switch (cam.preset) {
		case 'pushIn':
			return [
				{t: 0, x: cx, y: cy, zoom: 1, ease: 'linear' as const},
				{t: dur, x: cx, y: cy, zoom: 1 + 0.18 * a, ease: 'linear' as const},
			];
		case 'pullOut':
			return [
				{t: 0, x: cx, y: cy, zoom: 1 + 0.18 * a, ease: 'linear' as const},
				{t: dur, x: cx, y: cy, zoom: 1, ease: 'linear' as const},
			];
		case 'panLeft':
			return [
				{t: 0, x: cx + pan, y: cy, zoom: 1.08, ease: 'linear' as const},
				{t: dur, x: cx - pan, y: cy, zoom: 1.08, ease: 'linear' as const},
			];
		case 'panRight':
			return [
				{t: 0, x: cx - pan, y: cy, zoom: 1.08, ease: 'linear' as const},
				{t: dur, x: cx + pan, y: cy, zoom: 1.08, ease: 'linear' as const},
			];
		case 'panUp':
			return [
				{t: 0, x: cx, y: cy + pan, zoom: 1.08, ease: 'linear' as const},
				{t: dur, x: cx, y: cy - pan, zoom: 1.08, ease: 'linear' as const},
			];
		case 'panDown':
			return [
				{t: 0, x: cx, y: cy - pan, zoom: 1.08, ease: 'linear' as const},
				{t: dur, x: cx, y: cy + pan, zoom: 1.08, ease: 'linear' as const},
			];
		case 'drift':
			return [
				{t: 0, x: cx - pan * 0.3, y: cy + pan * 0.15, zoom: 1.04, ease: 'linear' as const},
				{t: dur, x: cx + pan * 0.3, y: cy - pan * 0.15, zoom: 1.1, ease: 'linear' as const},
			];
		default:
			return [];
	}
}

export function cameraAt(cam: Camera | undefined, t: number, W: number, H: number, dur: number): CamState {
	const base = {x: W / 2, y: H / 2, zoom: 1, rotate: 0};
	if (!cam) return base;
	const kfs = sortByT(cam.keyframes.length ? cam.keyframes : presetKeyframes(cam, W, H, dur));
	return {
		x: sample(kfs, 'x', t, base.x, (v) => px(v as never, W)),
		y: sample(kfs, 'y', t, base.y, (v) => px(v as never, H)),
		zoom: sample(kfs, 'zoom', t, 1),
		rotate: sample(kfs, 'rotate', t, 0),
	};
}

export function shakeAt(cam: Camera | undefined, t: number, seed: string): ShakeState {
	const s = {dx: 0, dy: 0, rotate: 0};
	if (!cam) return s;
	cam.shake.forEach((sh, i) => {
		if (t < sh.at || t > sh.at + sh.duration) return;
		const p = (t - sh.at) / sh.duration;
		// quick attack, then decay
		const env = sh.decay ? Math.min(1, p * 8) * Math.pow(1 - clamp01(p), 1.6) : 1;
		s.dx += noise1(`${seed}-sx-${i}`, t, sh.frequency) * sh.amplitude * env;
		s.dy += noise1(`${seed}-sy-${i}`, t, sh.frequency * 1.1) * sh.amplitude * env;
		s.rotate += noise1(`${seed}-sr-${i}`, t, sh.frequency * 0.6) * sh.rotate * env;
	});
	return s;
}

/**
 * CSS transform for a full-frame plane at parallax depth d.
 * depth 1 follows the camera exactly, 0 is screen-locked, >1 moves faster (foreground).
 * Use with transform-origin: 0 0.
 */
export function planeTransform(cam: CamState, d: number, W: number, H: number): string {
	const cx = W / 2 + (cam.x - W / 2) * d;
	const cy = H / 2 + (cam.y - H / 2) * d;
	const z = Math.max(0.01, 1 + (cam.zoom - 1) * d);
	const r = cam.rotate * d;
	return `translate(${W / 2}px, ${H / 2}px) rotate(${r}deg) scale(${z}) translate(${-cx}px, ${-cy}px)`;
}
