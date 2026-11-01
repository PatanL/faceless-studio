import React from 'react';
import {E, clamp} from '../lib/anim';
import {GunArt} from '../art/guns';
import {Sparkle} from '../art/props';

// S01 (0.00-2.90): AK-12 hero on a swirl sunburst + two title pills.

const CX = 540;
const CY = 1080;
const N = 16;
const K = 0.0019; // swirl: radians of twist per px of radius

function ray(i: number): string {
	const a0 = (i * 2 * Math.PI) / N;
	const w = (Math.PI / N) * 1.0;
	const pts1: string[] = [];
	const pts2: string[] = [];
	for (let r = 0; r <= 2400; r += 60) {
		const a1 = a0 + K * r;
		const a2 = a0 + w + K * r;
		pts1.push(`${(CX + Math.cos(a1) * r).toFixed(1)},${(CY + Math.sin(a1) * r).toFixed(1)}`);
		pts2.unshift(`${(CX + Math.cos(a2) * r).toFixed(1)},${(CY + Math.sin(a2) * r).toFixed(1)}`);
	}
	return `M${pts1.join(' L')} L${pts2.join(' L')} Z`;
}
const RAYS = Array.from({length: N}, (_, i) => ray(i));

const Pill: React.FC<{x: number; y: number; w: number; h: number; fill: string; edge: string; shadow: string; text: string; color: string; size: number; tw: number}> = ({x, y, w, h, fill, edge, shadow, text, color, size, tw}) => (
	<g transform={`translate(${x} ${y})`}>
		<rect x={9} y={9} width={w} height={h} rx={22} fill={shadow} />
		<rect x={0} y={0} width={w} height={h} rx={22} fill={fill} />
		<rect x={0} y={0} width={w} height={8} rx={4} fill={edge} />
		<text x={w / 2} y={h / 2 + size * 0.36} textAnchor="middle" fontFamily="MontserratXB" fontWeight={800} fontSize={size} fill={color} textLength={tw} lengthAdjust="spacingAndGlyphs">
			{text}
		</text>
	</g>
);

export const Hook: React.FC<{t: number}> = ({t}) => {
	const rot = t * 6;
	const bob = Math.sin((t / 2) * Math.PI * 2) * 6;
	const wob = Math.sin((t / 2) * Math.PI * 2 + 1) * 1;
	const p1 = E.outExpo(clamp((t - 0.13) / 0.37));
	const p2 = E.outExpo(clamp((t - 0.95) / 0.35));
	const gx = 520;
	const gy = 935 + bob;
	const gs = 2.05;
	// receiver / mag points for sparkles (gun-local -> screen)
	const pt = (lx: number, ly: number): [number, number] => {
		const a = ((-25 + wob) * Math.PI) / 180;
		return [gx + gs * (lx * Math.cos(a) - ly * Math.sin(a)), gy + gs * (lx * Math.sin(a) + ly * Math.cos(a))];
	};
	const sp1 = pt(-10, -14);
	const sp2 = pt(40, 70);
	return (
		<g>
			<rect x={0} y={0} width={1080} height={1920} fill="#F66D00" />
			<radialGradient id="hookCore" cx={CX} cy={CY} r={1300} gradientUnits="userSpaceOnUse">
				<stop offset="0" stopColor="#F9B421" />
				<stop offset="0.35" stopColor="#F8961A" />
				<stop offset="1" stopColor="#F77A0E" />
			</radialGradient>
			<g transform={`rotate(${rot} ${CX} ${CY})`}>
				{RAYS.map((d, i) => (
					<path key={i} d={d} fill="url(#hookCore)" />
				))}
			</g>
			<rect x={0} y={0} width={1080} height={1920} fill="url(#hatch)" />
			<rect x={0} y={0} width={1080} height={1920} fill="url(#hookVignette)" />
			<g transform={`translate(${gx} ${gy}) rotate(${-25 + wob}) scale(${gs})`}>
				<GunArt kind="ak12" />
				{/* under-barrel launcher, as on the hero rifle */}
				<rect x={56} y={16} width={104} height={26} rx={12} fill="#2B2F30" />
				<rect x={56} y={16} width={104} height={6} rx={3} fill="#4C4E48" />
				<rect x={30} y={18} width={30} height={22} rx={6} fill="#1F2224" />
			</g>
			<Sparkle t={t} t0={0.5} x={sp1[0]} y={sp1[1]} size={170} />
			<Sparkle t={t} t0={1.25} x={sp2[0]} y={sp2[1]} size={110} spin={-30} />
			{t >= 0.13 && (
				<g transform={`translate(${(1 - p1) * 1080} 0)`}>
					<Pill x={22} y={180} w={1036} h={148} fill="#EBD10D" edge="#EDD722" shadow="#63511B" text="WHY DID RUSSIA SWITCH" color="#2E2A12" size={84} tw={940} />
				</g>
			)}
			{t >= 0.95 && (
				<g transform={`translate(${(1 - p2) * 1080} 0)`}>
					<Pill x={93} y={352} w={890} h={146} fill="#E23536" edge="#E8504F" shadow="#AA2D23" text="TO THE AK-12 RIFLE?" color="#FCEDE6" size={78} tw={804} />
				</g>
			)}
		</g>
	);
};
