/**
 * Micro layer (bible §8): marine snow, plankton and micro-bubbles, ALWAYS present, 150-350 detectable specks
 * per frame. Bean-shaped (two unequal arcs, not ellipses), in 2-3 tints of the field, drifting with
 * per-particle noise and wrapping. Put one <Micro> on each of 3 planes (far / mid / subject) so the layer
 * drifts with parallax; per-plane presets scale size, opacity and count with depth.
 *
 * Detectability: the D3 counter keeps components 6-400 px that are > 12 luma above a ~60 px median
 * background. Far specks are 2.5-4 px (some fall below the counter, as they do in the references); mid and
 * subject specks are 4-9 px at opacity >= 0.55 so they clear the threshold even on the bright upper field.
 */
import React from 'react';
import {c, rgba} from '../../../kurz-style/engine/src/lib/color';
import {noise1, rand} from '../../../kurz-style/engine/src/lib/rng';
import {twinkle} from '../../../kurz-style/engine/src/motion/motion';
import {H, OVER, W} from '../../../kurz-style/engine/src/depth/Planes';

export type MicroPreset = {n: number; size: [number, number]; opacity: [number, number]; drift: [number, number]; plankton: number; bubbles: number; tints: string[]};

export const MICRO: Record<'far' | 'mid' | 'near', MicroPreset> = {
	far: {n: 90, size: [2.6, 4.4], opacity: [0.4, 0.75], drift: [3, -3], plankton: 0, bubbles: 0, tints: ['tide-5', 'tide-4', 'bone-1']},
	mid: {n: 85, size: [3.6, 6.4], opacity: [0.5, 0.85], drift: [5, -5], plankton: 0.12, bubbles: 0.05, tints: ['tide-5', 'bone-1', 'amber-5']},
	near: {n: 65, size: [5, 9.5], opacity: [0.55, 0.92], drift: [7, -8], plankton: 0.22, bubbles: 0.1, tints: ['bone-2', 'tide-5', 'amber-5']},
};

/** bean: a fat end and a thin end, length 1, centred */
const BEAN = 'M -0.5 0.02 C -0.52 -0.3 -0.12 -0.42 0.14 -0.3 C 0.42 -0.18 0.56 0.06 0.4 0.22 C 0.22 0.4 -0.06 0.2 -0.24 0.3 C -0.42 0.38 -0.48 0.22 -0.5 0.02 Z';

export const Micro: React.FC<{t: number; seed: string; preset: keyof typeof MICRO; n?: number; area?: [number, number, number, number]; keepOut?: (x: number, y: number) => boolean}> = ({
	t,
	seed,
	preset,
	n,
	area = [-OVER, -OVER, W + 2 * OVER, H + 2 * OVER],
	keepOut,
}) => {
	const P = MICRO[preset];
	const tint = (x: string) => c(x); // specks are light: never hazed toward a plane's ink
	const [ax, ay, aw, ah] = area;
	const cols = P.tints.map((x) => tint(x));
	const count = n ?? P.n;
	const out: React.ReactNode[] = [];
	for (let i = 0; i < count; i++) {
		const sp = 0.6 + rand(seed, i * 11) * 0.8;
		let x = ax + rand(seed, i * 11 + 1) * aw + P.drift[0] * sp * t + 12 * noise1(`${seed}${i}x`, t * 0.3);
		let y = ay + rand(seed, i * 11 + 2) * ah + P.drift[1] * sp * t + 9 * noise1(`${seed}${i}y`, t * 0.3);
		x = ax + ((((x - ax) % aw) + aw) % aw);
		y = ay + ((((y - ay) % ah) + ah) % ah);
		if (keepOut && keepOut(x, y)) continue;
		const s = P.size[0] + rand(seed, i * 11 + 3) * (P.size[1] - P.size[0]);
		const o = (P.opacity[0] + rand(seed, i * 11 + 4) * (P.opacity[1] - P.opacity[0])) * (0.75 + 0.25 * twinkle(t, seed, i));
		const rot = rand(seed, i * 11 + 5) * 360 + t * 25 * (rand(seed, i * 11 + 6) - 0.5);
		const kind = rand(seed, i * 11 + 7);
		const col = cols[i % cols.length];
		const tr = `translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${rot.toFixed(0)})`;
		if (kind < P.bubbles) {
			// micro-bubble: ring + glint
			out.push(
				<g key={i} transform={tr} opacity={o}>
					<circle r={s * 0.55} fill={rgba(c('tide-5'), 0.25)} stroke={c('tide-5')} strokeWidth={Math.max(1.2, s * 0.18)} />
					<circle cx={-s * 0.18} cy={-s * 0.18} r={Math.max(0.8, s * 0.12)} fill={c('bone-2')} />
				</g>,
			);
		} else if (kind < P.bubbles + P.plankton) {
			// plankton: a bean body with two hair-thin antennae and a tail dot (copepod-ish, generic)
			out.push(
				<g key={i} transform={`${tr} scale(${s.toFixed(2)})`} opacity={o}>
					<path d={BEAN} fill={col} />
					<path d="M 0.38 -0.08 Q 0.8 -0.5 1.1 -0.36 M 0.38 0.08 Q 0.8 0.42 1.08 0.4" stroke={col} strokeWidth={0.09} fill="none" strokeLinecap="round" />
					<circle cx={-0.72} cy={0.04} r={0.11} fill={col} />
				</g>,
			);
		} else {
			out.push(<path key={i} d={BEAN} fill={col} opacity={o} transform={`${tr} scale(${s.toFixed(2)} ${(s * (0.8 + rand(seed, i * 11 + 8) * 0.35)).toFixed(2)})`} />);
		}
	}
	return <g>{out}</g>;
};

