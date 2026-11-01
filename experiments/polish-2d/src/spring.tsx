/**
 * polish/Spring: wraps any registered component and replaces the kit's eased enter anims with
 * physically shaped ones [POLISH_IDEAS 4a-4d]. Everything is a pure function of time.
 *
 * kind "drop": gravity fall (ease-in), stretch along the fall, a volume-keeping squash on landing
 *   that springs back with a small overshoot. Replaces the kit's `drop` (bounce easing).
 * kind "pop": scale from 0 on a spring with overshoot; the vertical axis leads the horizontal by
 *   2 frames, so the figure stretches up and then fills out (follow-through). Replaces `pop` (backOut).
 * Both grow from the bottom centre (the thing stands or lands on something).
 *
 * props: inner (component name), innerProps, kind, at (scene s), fall (s), distance (px),
 * squash (0..1), damping, stiffness, mass, origin (CSS transform-origin, default bottom centre)
 */
import React from 'react';
import {spring} from 'remotion';
import {getComponent, type KitComponent} from '../../../studio/src/core/registry';

const n = (v: unknown, d: number) => (typeof v === 'number' && Number.isFinite(v) ? v : d);

export const Spring: KitComponent = (p) => {
	const {props, time, fps} = p;
	const Inner = getComponent(String(props.inner));
	if (!Inner) return null;
	const at = n(props.at, 0);
	const kind = props.kind === 'pop' ? 'pop' : 'drop';
	const cfg = {damping: n(props.damping, 11), stiffness: n(props.stiffness, 180), mass: n(props.mass, 0.6)};
	let ty = 0;
	let sx = 1;
	let sy = 1;
	let opacity = 1;
	const t = time - at;
	if (t < 0) return null;
	if (kind === 'drop') {
		const fall = n(props.fall, 0.22);
		const dist = n(props.distance, 90);
		const sq = n(props.squash, 0.2);
		opacity = Math.min(1, t / (2 / fps));
		if (t < fall) {
			const u = t / fall;
			ty = -dist * (1 - u * u); // gravity: position ~ t^2
			const v = (2 * u) / fall; // normalised speed
			sy = 1 + Math.min(0.14, 0.03 * v);
			sx = 1 / Math.sqrt(sy);
		} else {
			// landing: impulse that springs back to rest with one small overshoot
			const s = spring({frame: (t - fall) * fps, fps, config: cfg});
			sy = 1 - sq * (1 - s);
			sx = 1 / Math.sqrt(Math.max(0.5, sy));
		}
	} else {
		const s1 = spring({frame: t * fps, fps, config: cfg});
		const s2 = spring({frame: t * fps - 2, fps, config: cfg});
		sy = Math.max(0.0001, s1);
		sx = Math.max(0.0001, s2);
		opacity = Math.min(1, t / (3 / fps));
	}
	return (
		<div
			style={{
				position: 'absolute',
				inset: 0,
				opacity,
				transformOrigin: typeof props.origin === 'string' ? props.origin : '50% 100%',
				transform: `translateY(${ty}px) scale(${sx}, ${sy})`,
			}}
		>
			<Inner {...p} props={(props.innerProps as Record<string, unknown>) ?? {}} />
		</div>
	);
};
