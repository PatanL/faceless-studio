// Shared bench scene: a flat-2D explainer landscape (sky, far range, hills, a round creature, foreground
// plants) drawn as SVG. Each technique in Root.tsx adds ONE thing on top, so its render cost is the
// difference against `Base`. Everything is a pure function of the frame (Remotion renders out of order).
import React from 'react';
import {Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {noise2D} from '@remotion/noise';

export const W = 1080;
export const H = 1920;

export const C = {
	sky0: '#0b1d3a',
	sky1: '#21497a',
	far: '#36628f',
	mid: '#2a4f73',
	near: '#1c3a57',
	fg: '#0f2438',
	body: '#f2a541',
	bodyDark: '#c97a1e',
	rim: '#ffe8b0',
	glow: '#ffcf6b',
	ray: '#cfe9ff',
	haze: '#7fa6c9',
};

/** Camera: slow push plus a lateral drift, so parallax planes visibly separate. */
export const useCam = () => {
	const f = useCurrentFrame();
	const {durationInFrames} = useVideoConfig();
	const p = interpolate(f, [0, durationInFrames], [0, 1], {easing: Easing.bezier(0.65, 0, 0.35, 1)});
	return {zoom: 1 + 0.08 * p, x: -60 + 120 * p, y: 0};
};

/** transform for a full-frame plane at parallax depth d (1 = subject plane, 0 = screen-locked). */
export const planeT = (cam: {zoom: number; x: number; y: number}, d: number) => {
	const z = 1 + (cam.zoom - 1) * d;
	return `translate(${W / 2 - cam.x * d}px, ${H / 2 - cam.y * d}px) scale(${z}) translate(${-W / 2}px, ${-H / 2}px)`;
};

export const Sky: React.FC = () => (
	<>
		<defs>
			<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
				<stop offset="0" stopColor={C.sky0} />
				<stop offset="1" stopColor={C.sky1} />
			</linearGradient>
		</defs>
		<rect x={-200} y={-200} width={W + 400} height={H + 400} fill="url(#sky)" />
	</>
);

const ridge = (seed: string, base: number, amp: number, step = 60) => {
	let d = `M -300 ${H + 300} L -300 ${base}`;
	for (let x = -300; x <= W + 300; x += step) {
		d += ` L ${x} ${base - amp * (0.5 + 0.5 * noise2D(seed, x / 400, 0))}`;
	}
	return d + ` L ${W + 300} ${H + 300} Z`;
};
const FAR = ridge('far', 1100, 260);
const MID = ridge('mid', 1350, 200, 50);
const NEAR = ridge('near', 1560, 150, 40);

/** `haze` 0..1 mixes the plane toward the sky colour (atmospheric perspective: free, it is just a colour). */
export const Far: React.FC = () => <path d={FAR} fill={C.far} />;
export const Mid: React.FC = () => <path d={MID} fill={C.mid} />;
export const Near: React.FC = () => <path d={NEAR} fill={C.near} />;

const PLANTS = Array.from({length: 9}, (_, i) => ({
	x: -100 + i * 150 + random(`pl-x${i}`) * 80,
	h: 260 + random(`pl-h${i}`) * 260,
	w: 40 + random(`pl-w${i}`) * 40,
}));
export const Foreground: React.FC = () => {
	const f = useCurrentFrame();
	return (
		<g>
			{PLANTS.map((p, i) => {
				const sway = Math.sin(f / 30 + i) * 6; // secondary motion: tips lag the base
				return (
					<path
						key={i}
						d={`M ${p.x} ${H + 40} Q ${p.x + sway} ${H - p.h / 2} ${p.x + sway * 2.2} ${H - p.h} Q ${p.x + p.w + sway} ${H - p.h / 2} ${p.x + p.w} ${H + 40} Z`}
						fill={C.fg}
					/>
				);
			})}
		</g>
	);
};

/** The subject: a round creature with spring entrance, squash/stretch, breathing and blinks. */
export const Creature: React.FC<{rim?: boolean}> = ({rim}) => {
	const f = useCurrentFrame();
	const {fps} = useVideoConfig();
	// anticipation (dip) -> spring jump with overshoot -> settle
	const jump = spring({frame: f - 10, fps, config: {damping: 11, stiffness: 120, mass: 0.8}});
	const antic = interpolate(f, [0, 6, 10], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
	const y = 1180 - 120 * jump + 30 * antic;
	const vel = jump - spring({frame: f - 11, fps, config: {damping: 11, stiffness: 120, mass: 0.8}});
	const stretch = 1 + Math.max(-0.12, Math.min(0.18, vel * 3)) - antic * 0.1; // squash/stretch from velocity, volume kept
	const breathe = 1 + 0.015 * Math.sin((f / fps) * Math.PI * 2 * 0.25);
	const sy = stretch * breathe;
	const sx = 1 / Math.sqrt(sy);
	// blink: 4-frame close/open every ~3.2 s, phase-locked to a constant
	const bp = (f + 17) % 96;
	const lid = bp < 4 ? [1, 0.2, 0.05, 0.6][bp] : 1;
	const r = 170;
	return (
		<g transform={`translate(540 ${y}) scale(${sx} ${sy})`}>
			<defs>
				<radialGradient id="cr-body" cx="0.38" cy="0.32" r="0.8">
					<stop offset="0" stopColor="#ffd27a" />
					<stop offset="0.6" stopColor={C.body} />
					<stop offset="1" stopColor={C.bodyDark} />
				</radialGradient>
				<clipPath id="cr-clip">
					<circle r={r} />
				</clipPath>
			</defs>
			<circle r={r} fill="url(#cr-body)" />
			{rim ? (
				// rim light: the silhouette stroke shifted AWAY from the light (key at upper left), clipped to the body: only the lit edge shows
				<g clipPath="url(#cr-clip)">
					<circle r={r} fill="none" stroke={C.rim} strokeWidth={22} opacity={0.85} transform="translate(10 14)" />
					<circle r={r} fill={C.bodyDark} opacity={0.0} />
				</g>
			) : null}
			<ellipse cx={-55} cy={-30} rx={22} ry={30 * lid} fill="#1a1a2e" />
			<ellipse cx={55} cy={-30} rx={22} ry={30 * lid} fill="#1a1a2e" />
			<path d="M -40 50 Q 0 80 40 50" stroke="#1a1a2e" strokeWidth={9} fill="none" strokeLinecap="round" />
		</g>
	);
};

export const creatureY = (f: number, fps: number) =>
	1180 - 120 * spring({frame: f - 10, fps, config: {damping: 11, stiffness: 120, mass: 0.8}});

/** Caption-like text so the font rasteriser is part of every frame's cost. */
export const Caption: React.FC = () => {
	const f = useCurrentFrame();
	const words = 'If you fell into the sun you would vanish in seconds'.split(' ');
	const n = Math.min(words.length, Math.floor(f / 8) + 1);
	return (
		<div
			style={{
				position: 'absolute',
				left: 150,
				width: 780,
				top: 1330,
				textAlign: 'center',
				fontFamily: 'sans-serif',
				fontWeight: 800,
				fontSize: 72,
				color: 'white',
				textShadow: '0 4px 16px rgba(0,0,0,0.6)',
			}}
		>
			{words.slice(Math.max(0, n - 4), n).join(' ')}
		</div>
	);
};
