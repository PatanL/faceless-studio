// Shared helpers for the horror kit: prop parsing, cue envelopes, timelines, palette.
import React, {useId} from 'react';
import {random} from 'remotion';
import {clamp01, ease} from '../../core/anim';

export const num = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);
export const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);
export const bool = (v: unknown, d: boolean) => (typeof v === 'boolean' ? v : d);
export const arr = <T = Record<string, unknown>,>(v: unknown): T[] => (Array.isArray(v) ? (v as T[]) : []);
export const obj = (v: unknown): Record<string, unknown> =>
	v && typeof v === 'object' && !Array.isArray(v) ? (v as Record<string, unknown>) : {};

/** SVG-safe unique id per component instance (React ids contain colons / guillemets). */
export const useUid = (prefix: string) => prefix + useId().replace(/[^a-zA-Z0-9]/g, '');

export {clamp01, ease, random};

/** Muted night palette shared by backgrounds, phone and characters. */
export const P = {
	ink: '#15141a',
	line: '#1b1a20',
	night: '#0d1118',
	wallDark: '#1f2530',
	wall: '#2b3240',
	wallLight: '#3a4352',
	floor: '#1a1d24',
	wood: '#3b2f2a',
	woodLight: '#4d3d34',
	metal: '#5d6570',
	metalLight: '#8a929c',
	moon: '#9fb6cf',
	warm: '#d9a560',
	sick: '#9fbf8f',
	red: '#e0313a',
	redGlow: 'rgba(255,40,50,0.65)',
	exit: '#46d17a',
	skin: '#e6d7c3',
	skinShade: '#c7b49d',
	handSkin: '#c9b7a3',
};

export type Cue = {at: number; duration?: number; amount?: number};

/**
 * Envelope of a list of cues at time t: 0 outside every cue, ramps in/out over `fade`
 * seconds inside one, scaled by the cue's amount. Returns the strongest active cue.
 */
export function cueLevel(cues: unknown, t: number, defDur = 0.4, fade = 0.06): number {
	let best = 0;
	for (const c of arr<Cue>(cues)) {
		const at = num(c.at, 0);
		const d = num(c.duration, defDur);
		if (t < at || t > at + d) continue;
		const f = Math.max(0.0001, Math.min(fade, d / 2));
		const env = Math.min(1, (t - at) / f, (at + d - t) / f);
		best = Math.max(best, env * num(c.amount, 1));
	}
	return best;
}

/** Latest entry of a [{t, ...}] list whose t <= time (or the first one). */
export function atTime<T extends {t?: number}>(list: T[], time: number): {item: T | undefined; since: number; index: number} {
	let item: T | undefined;
	let since = 0;
	let index = -1;
	list.forEach((e, i) => {
		const et = num(e.t, 0);
		if (et <= time) {
			item = e;
			since = time - et;
			index = i;
		}
	});
	if (!item && list.length) return {item: list[0], since: 0, index: 0};
	return {item, since, index};
}

/** Pop-in progress for something that appears at `at` (0 before, 1 after `dur`). */
export const popIn = (t: number, at: number, dur = 0.28) => clamp01((t - at) / dur);

/** Deterministic stepped random in [-1, 1] that changes every `step` seconds. */
export const jitter = (seed: string, t: number, step = 1 / 15) => random(`${seed}-${Math.floor(t / step)}`) * 2 - 1;

/** Full-box SVG for backgrounds: 1080x1920 art that crops (slice) to any box. */
export const Stage: React.FC<{width: number; height: number; children: React.ReactNode; vb?: string}> = ({
	width,
	height,
	children,
	vb = '0 0 1080 1920',
}) => (
	<svg width={width} height={height} viewBox={vb} preserveAspectRatio="xMidYMid slice" style={{display: 'block'}}>
		{children}
	</svg>
);
