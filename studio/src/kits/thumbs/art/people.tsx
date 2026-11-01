// Tiny humans for scale + the horror "big subject" figure. All flat, no red.
import React from 'react';
import {bezier, taper, type Pt} from '../fx';

/**
 * Scuba diver swimming toward +x, ~200 x 90 units, centred on (x, y), scaled by `s`.
 * Flashlight beam points along `beamAngle` (deg, 0 = +x).
 */
export const Diver: React.FC<{x: number; y: number; s: number; flip?: boolean; beam?: number; beamAngle?: number; id: string; tilt?: number}> = ({
	x,
	y,
	s,
	flip,
	beam = 0,
	beamAngle = 0,
	id,
	tilt = -8,
}) => {
	const c = '#e8e8e8';
	return (
		<g transform={`translate(${x} ${y}) scale(${flip ? -s : s} ${s}) rotate(${tilt})`}>
			<defs>
				<linearGradient id={`${id}-beam`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#fffbe6" stopOpacity={0.85} />
					<stop offset="1" stopColor="#fffbe6" stopOpacity={0} />
				</linearGradient>
			</defs>
			{beam > 0 && (
				<g transform={`translate(92 -4) rotate(${beamAngle + 8})`}>
					<polygon points={`0,-5 ${beam},${-beam * 0.32} ${beam},${beam * 0.32} 0,5`} fill={`url(#${id}-beam)`} />
				</g>
			)}
			{/* fins */}
			<path d="M-96 6 L-140 -14 L-136 10 Z M-96 18 L-142 22 L-128 40 Z" fill={c} />
			{/* legs */}
			<path d={taper([[-30, 8], [-64, 10], [-98, 10]], 18, 11)} fill={c} />
			<path d={taper([[-30, 16], [-62, 24], [-96, 28]], 18, 11)} fill={c} />
			{/* torso */}
			<path d={taper([[-34, 10], [0, 2], [34, -2]], 30, 26)} fill={c} />
			{/* tank */}
			<rect x={-28} y={-26} width={52} height={16} rx={8} fill="#9a9a9a" stroke="#000" strokeWidth={2} />
			{/* head + mask */}
			<circle cx={50} cy={-6} r={15} fill={c} />
			<rect x={52} y={-14} width={14} height={10} rx={3} fill="#111" />
			{/* arm with torch */}
			<path d={taper([[24, 4], [56, 8], [84, -2]], 10, 8)} fill={c} />
			<rect x={80} y={-9} width={18} height={10} rx={2} fill="#bbb" stroke="#000" strokeWidth={1.5} />
			{/* bubbles */}
			<circle cx={62} cy={-34} r={4} fill="none" stroke="#fff" strokeWidth={2} />
			<circle cx={70} cy={-52} r={3} fill="none" stroke="#fff" strokeWidth={2} />
			<circle cx={64} cy={-68} r={2} fill="none" stroke="#fff" strokeWidth={2} />
		</g>
	);
};

/** Standing person (front), ~60 x 180 units with feet at (x, y). */
export const Person: React.FC<{x: number; y: number; h: number; color?: string; outline?: string}> = ({x, y, h, color = '#f2f2f2', outline = '#000'}) => {
	const s = h / 180;
	return (
		<g transform={`translate(${x} ${y}) scale(${s})`} stroke={outline} strokeWidth={3 / s > 6 ? 6 : 3}>
			<circle cx={0} cy={-158} r={20} fill={color} />
			<path d="M-22 -134 C-26 -100 -26 -80 -22 -60 L22 -60 C26 -80 26 -100 22 -134 Z" fill={color} />
			<path d="M-20 -62 L-16 0 L-4 0 L0 -40 L4 0 L16 0 L20 -62 Z" fill={color} />
			<path d="M-22 -130 L-34 -70 L-26 -68 L-14 -118 Z M22 -130 L34 -70 L26 -68 L14 -118 Z" fill={color} />
		</g>
	);
};

/**
 * Horror resident seen from behind, holding a glowing phone. ~70 x 190 units, feet at (x, y).
 * `glow` adds the phone light on the face side.
 */
export const Resident: React.FC<{x: number; y: number; h: number; id: string; glow?: boolean; tone?: string; flip?: boolean}> = ({
	x,
	y,
	h,
	id,
	glow = true,
	tone = '#c7b447',
	flip,
}) => {
	const hair = '#0c0e0f';
	const pants = '#283034';
	const s = h / 190;
	return (
		<g transform={`translate(${x} ${y}) scale(${flip ? -s : s} ${s})`}>
			<defs>
				<radialGradient id={`${id}-pg`}>
					<stop offset="0" stopColor="#d8f3ff" stopOpacity={0.9} />
					<stop offset="1" stopColor="#d8f3ff" stopOpacity={0} />
				</radialGradient>
			</defs>
			{glow && <circle cx={26} cy={-118} r={60} fill={`url(#${id}-pg)`} />}
			{/* hair/head */}
			<path d="M-20 -160 C-22 -186 22 -190 22 -162 C24 -146 16 -136 0 -134 C-14 -134 -22 -146 -20 -160 Z" fill={hair} />
			{/* hoodie torso */}
			<path d="M-30 -132 C-40 -120 -40 -80 -36 -60 L36 -60 C40 -80 40 -120 30 -132 C16 -138 -16 -138 -30 -132 Z" fill={tone} />
			{/* legs */}
			<path d="M-26 -62 L-22 0 L-6 0 L0 -36 L6 0 L22 0 L26 -62 Z" fill={pants} />
			<path d="M-30 -132 C-40 -120 -40 -80 -36 -60 L-20 -60 C-24 -90 -22 -118 -14 -134 Z" fill="#000" opacity={0.35} />
			{/* arm raised with phone */}
			<path d="M28 -126 C46 -110 44 -96 30 -92 L24 -104 Z" fill={tone} />
			<rect x={22} y={-128} width={16} height={26} rx={3} fill="#e9f8ff" />
			{/* rim light */}
			<path d="M30 -132 C40 -120 40 -80 36 -60" fill="none" stroke="#e8f7ff" strokeWidth={4} opacity={0.9} />
			<path d="M22 -162 C24 -146 16 -136 4 -134" fill="none" stroke="#e8f7ff" strokeWidth={4} opacity={0.9} />
			<path d="M-20 -160 C-22 -186 22 -190 22 -162" fill="none" stroke="#e8f7ff" strokeWidth={3} opacity={0.6} />
		</g>
	);
};

/**
 * Tall shadow figure ("the thing at the door"): too-long limbs, head tilted, white eyes and a
 * thin smile. Drawn in a 400 x 1000 box with feet at the bottom; `lean` tilts the head.
 */
export const ShadowFigure: React.FC<{x: number; y: number; w: number; h: number; id: string; tone?: string; lean?: number; eyes?: string}> = ({
	x,
	y,
	w,
	h,
	id,
	tone = '#020304',
	lean = 14,
	eyes = '#f6f6f0',
}) => {
	const armL: Pt[] = bezier([140, 300], [90, 480], [70, 700], [96, 900], 30);
	const armR: Pt[] = bezier([260, 300], [320, 500], [330, 700], [300, 880], 30);
	return (
		<svg x={x} y={y} width={w} height={h} viewBox="0 0 400 1000" overflow="visible" preserveAspectRatio="xMidYMax meet">
			<defs>
				<filter id={`${id}-eg`} x="-200%" y="-200%" width="500%" height="500%">
					<feGaussianBlur stdDeviation="7" />
				</filter>
				<filter id={`${id}-soft`} x="-20%" y="-20%" width="140%" height="140%">
					<feGaussianBlur stdDeviation="3" />
				</filter>
			</defs>
			<g filter={`url(#${id}-soft)`} fill={tone}>
				{/* body */}
				<path d="M130 290 C110 420 120 560 150 720 L140 1000 L190 1000 L200 760 L212 1000 L262 1000 L252 720 C282 560 292 420 270 290 C240 262 160 262 130 290 Z" />
				<path d={taper(armL, 36, 16)} />
				<path d={taper(armR, 36, 16)} />
				{/* long fingers */}
				{[-14, -4, 6, 16].map((o, i) => (
					<path key={`l${i}`} d={taper([[96, 890], [90 + o, 950], [84 + o * 1.6, 1000]], 8, 3)} />
				))}
				{[-14, -4, 6, 16].map((o, i) => (
					<path key={`r${i}`} d={taper([[300, 872], [304 + o, 930], [306 + o * 1.6, 975]], 8, 3)} />
				))}
				{/* neck + head, tilted */}
				<g transform={`rotate(${lean} 200 270)`}>
					<path d="M186 290 L190 220 L212 220 L216 290 Z" />
					<ellipse cx={200} cy={160} rx={62} ry={84} />
				</g>
			</g>
			<g transform={`rotate(${lean} 200 270)`}>
				<g filter={`url(#${id}-eg)`} opacity={0.9}>
					<ellipse cx={176} cy={150} rx={16} ry={10} fill={eyes} />
					<ellipse cx={226} cy={150} rx={16} ry={10} fill={eyes} />
				</g>
				<ellipse cx={176} cy={150} rx={11} ry={6} fill={eyes} />
				<ellipse cx={226} cy={150} rx={11} ry={6} fill={eyes} />
				<path d="M160 196 C185 214 215 214 240 194" fill="none" stroke={eyes} strokeWidth={3} opacity={0.75} />
			</g>
		</svg>
	);
};
