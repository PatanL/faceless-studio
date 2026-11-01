import React from 'react';
import {E, clamp} from '../lib/anim';
import {G, GunArt} from '../art/guns';
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
	const gs = 2.0;
	const gsy = 1.78; // slimmer than uniform: the reference rifle reads long and lean
	// receiver / mag points for sparkles (gun-local -> screen)
	const pt = (lx: number, ly: number): [number, number] => {
		const a = ((-25 + wob) * Math.PI) / 180;
		return [gx + gs * lx * Math.cos(a) - gsy * ly * Math.sin(a), gy + gs * lx * Math.sin(a) + gsy * ly * Math.cos(a)];
	};
	// v2: more and bigger glints, travelling along the rifle (receiver, muzzle, stock, magazine)
	const SPARKS: [number, number, number, number, number][] = [
		[0.3, -10, -14, 250, 30],
		[0.62, 150, -20, 170, -30],
		[0.95, -150, 10, 210, 30],
		[1.2, 40, 70, 270, -30],
		[1.55, 100, -24, 200, 30],
		[1.9, -60, -20, 240, -30],
		[2.25, 180, -10, 180, 30],
		[2.5, 30, 60, 220, -30],
	];
	// title pills clear out to the left just before the S02 matte arrives (2.97)
	const out = E.inCubic(clamp((t - 2.84) / 0.16)) * -1150;
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
			<g transform={`translate(${gx} ${gy}) rotate(${-25 + wob}) scale(${gs} ${gsy})`}>
				{/* under-barrel launcher, as on the hero rifle */}
				<rect x={28} y={16} width={36} height={24} rx={6} fill={G.g0} />
				<rect x={56} y={15} width={110} height={30} rx={13} fill={G.g2} />
				<rect x={56} y={15} width={110} height={9} rx={4.5} fill={G.g3} />
				<rect x={62} y={15} width={98} height={2.4} rx={1.2} fill={G.g4} />
				<rect x={156} y={18} width={14} height={24} rx={4} fill={G.g1} />
				<rect x={80} y={30} width={40} height={5} rx={2.5} fill={G.g0} />
				<path d="M40,40 L52,40 L50,58 Q46,62 42,58 Z" fill={G.g1} />
				<GunArt kind="ak12" lod={2} />
			</g>
			{SPARKS.map(([t0, lx, ly, size, spin], i) => {
				const [sx, sy] = pt(lx, ly);
				return <Sparkle key={i} t={t} t0={t0} x={sx} y={sy} size={size} spin={spin} dur={0.55} />;
			})}
			{t >= 0.13 && (
				<g transform={`translate(${(1 - p1) * 1080 + out} 0)`}>
					<Pill x={22} y={180} w={1036} h={148} fill="#EBD10D" edge="#EDD722" shadow="#63511B" text="WHY DID RUSSIA SWITCH" color="#2E2A12" size={84} tw={940} />
				</g>
			)}
			{t >= 0.95 && (
				<g transform={`translate(${(1 - p2) * 1080 + out * 1.1} 0)`}>
					<Pill x={93} y={352} w={890} h={146} fill="#E23536" edge="#E8504F" shadow="#AA2D23" text="TO THE AK-12 RIFLE?" color="#FCEDE6" size={78} tw={804} />
				</g>
			)}
		</g>
	);
};
