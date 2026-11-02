import React from 'react';
import {random} from 'remotion';
import {clamp01, ease} from './anim';
import type {SceneTiming, Transition} from './schema';

export type TransitionLook = {
	style: React.CSSProperties;
	/** Black overlay opacity drawn above the scene (dipBlack). */
	black: number;
	/** White flash overlay opacity (glitch). */
	flash: number;
	filter: React.ReactNode;
};

const DIRS = {
	left: [-1, 0],
	right: [1, 0],
	up: [0, -1],
	down: [0, 1],
} as const;

/**
 * Visual state of a scene during its incoming and outgoing transitions.
 * f = frame inside the scene's Sequence (0 = first rendered frame, including pre-roll).
 */
export function transitionLook(
	timing: SceneTiming,
	f: number,
	W: number,
	H: number,
	id: string,
): TransitionLook {
	const look: TransitionLook = {style: {}, black: 0, flash: 0, filter: null};
	let inP: number | null = null;
	let outP: number | null = null;
	if (timing.inFrames > 0 && f < timing.inFrames) inP = clamp01(f / timing.inFrames);
	const outStart = timing.pre + timing.frames - Math.floor(timing.outFrames / 2);
	if (timing.outT && timing.outFrames > 0 && f >= outStart) outP = clamp01((f - outStart) / timing.outFrames);

	const apply = (tr: Transition, p: number, incoming: boolean) => {
		switch (tr.type) {
			case 'cut':
				return;
			case 'fade':
				if (incoming) look.style.opacity = ease('inOut', p);
				return;
			case 'dipBlack':
				if (incoming) look.style.opacity = clamp01((p - 0.5) * 2);
				else look.black = clamp01(p * 2);
				return;
			case 'whip': {
				const [dx, dy] = DIRS[tr.direction];
				const e = ease('inOut', p);
				const k = incoming ? 1 - e : -e;
				// incoming slides in from the opposite side of the motion
				const tx = incoming ? -dx * W * k : dx * W * -k;
				const ty = incoming ? -dy * H * k : dy * H * -k;
				look.style.transform = `translate(${tx}px, ${ty}px)`;
				const blur = Math.sin(Math.PI * p) * 70;
				if (blur > 0.5) {
					const fid = `whip-${id}`;
					look.style.filter = `url(#${fid})`;
					look.filter = (
						<filter id={fid} x="-20%" y="-20%" width="140%" height="140%">
							<feGaussianBlur stdDeviation={dx !== 0 ? `${blur} 0` : `0 ${blur}`} />
						</filter>
					);
				}
				return;
			}
			case 'iris': {
				// incoming opens from a soft circle at the frame's upper-middle focus (a light/lens reveal); outgoing holds
				if (!incoming) return;
				const e = ease('inOut', p);
				const r = 2 + e * 118;
				look.style.clipPath = p >= 1 ? undefined : `circle(${r.toFixed(2)}% at 50% 42%)`;
				return;
			}
			case 'wipe': {
				// incoming rises behind a wavy water-line edge (a swell / bubble wipe); outgoing holds underneath
				if (!incoming) return;
				const e = ease('inOut', p);
				if (p >= 1) return;
				const pts: string[] = [];
				const n = 14;
				const dir = tr.direction;
				for (let i = 0; i <= n; i++) {
					const u = (i / n) * 100;
					const wv = Math.sin(i * 1.3 + p * 9) * 2.2 + Math.sin(i * 0.55 - p * 5) * 1.4;
					const edge = (1 - e) * 112 - 6 + wv;
					if (dir === 'left' || dir === 'right') pts.push(dir === 'left' ? `${edge.toFixed(2)}% ${u}%` : `${(100 - edge).toFixed(2)}% ${u}%`);
					else pts.push(dir === 'up' ? `${u}% ${edge.toFixed(2)}%` : `${u}% ${(100 - edge).toFixed(2)}%`);
				}
				const far = dir === 'left' ? ['120% 100%', '120% 0%'] : dir === 'right' ? ['-20% 100%', '-20% 0%'] : dir === 'up' ? ['100% 120%', '0% 120%'] : ['100% -20%', '0% -20%'];
				look.style.clipPath = `polygon(${[...pts, ...far].join(', ')})`;
				return;
			}
			case 'glitch': {
				// outgoing glitches up to the midpoint, incoming takes over glitching back down
				const amt = incoming ? 1 - clamp01((p - 0.5) * 2) : clamp01(p * 2);
				if (incoming && p < 0.5) {
					look.style.opacity = 0;
					return;
				}
				const step = Math.floor(f / 2);
				const fid = `glitch-${id}`;
				const shift = amt * 36;
				const seed = Math.floor(random(`${id}-g-${step}`) * 1000);
				look.style.filter = `url(#${fid})`;
				look.flash = Math.abs(p - 0.5) < 0.08 ? 0.35 : 0;
				look.filter = (
					<filter id={fid} x="-5%" y="0%" width="110%" height="100%" colorInterpolationFilters="sRGB">
						<feTurbulence type="fractalNoise" baseFrequency="0.00001 0.035" numOctaves={1} seed={seed} result="n" />
						<feComponentTransfer in="n" result="q">
							<feFuncR type="discrete" tableValues="0.1 0.5 0.5 0.9 0.5 0.3 0.5 0.7" />
						</feComponentTransfer>
						<feColorMatrix in="q" type="matrix" values="1 0 0 0 0  0 0 0 0 0.5  0 0 0 0 0  0 0 0 0 1" result="m" />
						<feDisplacementMap in="SourceGraphic" in2="m" scale={amt * 220} xChannelSelector="R" yChannelSelector="G" result="d" />
						<feColorMatrix in="d" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
						<feOffset in="r" dx={shift} dy={0} result="r2" />
						<feColorMatrix in="d" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="gb" />
						<feOffset in="gb" dx={-shift} dy={0} result="gb2" />
						<feBlend in="r2" in2="gb2" mode="screen" />
					</filter>
				);
				return;
			}
		}
	};
	if (inP !== null) apply(timing.inT, inP, true);
	if (outP !== null && timing.outT) apply(timing.outT, outP, false);
	return look;
}
