import React, {useId} from 'react';
import {P} from './defs';
import {ANCH, Gun, GunPose, gunPt} from './guns';
import type {Mouth} from '../lib/anim';

// Cut-out soldier puppet in the reference's construction: flat fills, no outlines, one darker
// shadow-side shape per part, lighter top-edge strips, capsule camo, skin-circle hands.
// Local frame: feet on y=0, ~610 units tall, facing +x (mirrored for -1).

export type Beard = 'full' | 'goatee' | 'moustache' | 'none' | 'stubble';
export type Look = {
	hair: string;
	beard: Beard;
	beardColor?: string;
	eye: string;
	patch: 'ru' | 'ua' | 'none';
	camo: 'ru' | 'ua' | 'off';
	head: 'helmet' | 'cap';
	hairFringe?: boolean;
	/** v3 hair mass under the helmet: crop = dark block at the back + sideburn, side = crop + a short
	 *  fringe tuft, swoop = a big fringe sweeping diagonally across the forehead */
	hairStyle?: 'crop' | 'side' | 'swoop';
	skin?: string;
	/** body build: w = torso/shoulder width factor, belly = 0..1 paunch, leg = trouser width factor */
	build?: {w?: number; belly?: number; leg?: number};
	brow?: string;
};
export type Brows = 'neutral' | 'angry' | 'worried' | 'happy' | 'raised';
export type Hand = [number, number] | 'grip' | 'fore' | 'side' | 'hidden';

export type Pose = {
	facing?: 1 | -1;
	legs?: 'stand' | 'kneel' | 'march' | 'none';
	legPhase?: number;
	crouch?: number;
	lean?: number;
	bob?: number;
	breathe?: number;
	headRot?: number;
	headX?: number;
	headY?: number;
	mouth?: Mouth;
	brows?: Brows;
	eyes?: 'open' | 'closed' | 'hearts';
	heartPulse?: number;
	lookX?: number;
	lookY?: number;
	gun?: GunPose | null;
	handN?: Hand; // near hand (screen-left when facing +1)
	handF?: Hand; // far hand
	pointN?: boolean;
	pointF?: boolean;
	sweat?: boolean;
	carrier?: boolean;
	/** v3 acting: extra foot spread (units, + = wider), and the pointing finger's angle (deg, 0 = +x) */
	stance?: number;
	pointAng?: number;
	/** hide the head (receiver close-ups where the face must stay out of frame) */
	noHead?: boolean;
	/** scale of the near hand circle (the S15 fumbling-hand gag) */
	handNScale?: number;
};

export const LOOKS: Record<string, Look> = {
	A: {hair: '#1F1D18', hairStyle: 'crop', beard: 'full', beardColor: '#1E1C19', eye: P.eyeGreen, patch: 'ru', camo: 'ru', head: 'helmet'},
	B: {hair: '#5A3418', hairStyle: 'side', beard: 'goatee', beardColor: '#6B3B1E', eye: P.eyeGreen, patch: 'ru', camo: 'ru', head: 'helmet', hairFringe: true},
	C: {hair: '#1F1D18', hairStyle: 'crop', beard: 'full', beardColor: '#1E1C19', eye: '#6E7A1E', patch: 'ru', camo: 'ru', head: 'helmet'},
	D: {hair: '#2A1B12', hairStyle: 'side', beard: 'moustache', beardColor: '#3A2214', eye: P.eyeGreen, patch: 'ru', camo: 'ru', head: 'helmet'},
	E: {hair: '#7A5430', hairStyle: 'swoop', beard: 'goatee', beardColor: '#6B4A2A', eye: P.eyeGreen, patch: 'ru', camo: 'ru', head: 'helmet', hairFringe: true},
	F: {hair: '#D6AE68', hairStyle: 'swoop', beard: 'moustache', beardColor: '#5A3420', eye: P.eyeBlue, patch: 'ua', camo: 'ru', head: 'helmet', hairFringe: true},
	G: {hair: '#4A2E1A', hairStyle: 'side', beard: 'full', beardColor: '#5A3420', eye: P.eyeBlue, patch: 'ua', camo: 'ua', head: 'helmet'},
	Blond: {hair: '#E8B85A', hairStyle: 'swoop', beard: 'none', eye: P.eyeBlue, patch: 'ru', camo: 'ru', head: 'helmet', hairFringe: true},
	Off: {hair: '#4A3020', hairStyle: 'crop', beard: 'goatee', beardColor: '#5A3420', eye: P.eyeGreen, patch: 'ru', camo: 'off', head: 'cap', build: {w: 1.22, belly: 1, leg: 1.12}},
	H: {hair: '#2A1C14', hairStyle: 'crop', beard: 'stubble', eye: P.eyeGreen, patch: 'ru', camo: 'ru', head: 'helmet'},
};

const ANCH_GRIP = Object.fromEntries(Object.entries(ANCH).map(([k, v]) => [k, v.grip])) as Record<string, [number, number]>;
const ANCH_FORE = Object.fromEntries(Object.entries(ANCH).map(([k, v]) => [k, v.fore])) as Record<string, [number, number]>;

const deg = (r: number) => (r * 180) / Math.PI;

/** Two-bone IK. bend=+1/-1 picks the elbow side. Stretches if out of reach so hands never detach. */
export function ik(s: [number, number], h: [number, number], l1: number, l2: number, bend: number): [number, number] {
	const dx = h[0] - s[0];
	const dy = h[1] - s[1];
	let d = Math.hypot(dx, dy);
	let k = 1;
	if (d > (l1 + l2) * 0.995) k = d / ((l1 + l2) * 0.995);
	l1 *= k;
	l2 *= k;
	d = Math.max(Math.abs(l1 - l2) + 0.01, Math.min(d, l1 + l2 - 0.01));
	const a = Math.acos(Math.max(-1, Math.min(1, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d))));
	const base = Math.atan2(dy, dx);
	const e = base + bend * a;
	return [s[0] + l1 * Math.cos(e), s[1] + l1 * Math.sin(e)];
}

export const Flag: React.FC<{kind: 'ru' | 'ua'; x: number; y: number; w: number; h: number; r?: number}> = ({kind, x, y, w, h, r = 4}) => {
	const cols = kind === 'ru' ? [P.ruWhite, P.ruBlue, P.ruRed] : [P.uaBlue, P.uaYellow];
	const n = cols.length;
	const id = useId().replace(/:/g, '');
	return (
		<g>
			<rect x={x - 3} y={y - 3} width={w + 6} height={h + 6} rx={r + 2} fill="#9C9C9C" />
			<clipPath id={`fl${id}`}>
				<rect x={x} y={y} width={w} height={h} rx={r} />
			</clipPath>
			<g clipPath={`url(#fl${id})`}>
				{cols.map((c, i) => (
					<rect key={i} x={x} y={y + (i * h) / n} width={w} height={h / n + 0.5} fill={c} />
				))}
				<rect x={x} y={y + h * 0.72} width={w} height={h * 0.28} fill="rgba(0,0,0,0.08)" />
			</g>
		</g>
	);
};

const Boot: React.FC<{x: number; y: number; rot?: number; s?: number}> = ({x, y, rot = 0, s = 1}) => (
	<g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
		<rect x={-31} y={-16} width={62} height={44} rx={8} fill={P.boot} />
		<path d="M-36,16 L36,16 Q70,18 72,42 L72,50 Q72,56 64,56 L-36,56 Q-42,56 -42,48 L-42,24 Q-42,16 -36,16 Z" fill={P.boot} />
		<path d="M10,18 L36,17 Q60,19 66,32 Q44,28 10,26 Z" fill={P.bootTop} opacity={0.9} />
		<rect x={-42} y={47} width={114} height={10} rx={4} fill="#0E0D0B" />
		<rect x={-32} y={-18} width={64} height={12} rx={5} fill={P.bootTop} />
	</g>
);

function camoFill(look: Look) {
	return look.camo === 'ua' ? 'url(#camoUA)' : look.camo === 'off' ? 'url(#camoOff)' : 'url(#camoRU)';
}
function camoDark(look: Look) {
	return look.camo === 'ua' ? 'url(#camoUAdk)' : 'url(#camoRUdk)';
}

const Eye: React.FC<{x: number; y: number; c: string; lx: number; ly: number; state: 'open' | 'closed' | 'hearts'; pulse: number}> = ({x, y, c, lx, ly, state, pulse}) => {
	if (state === 'closed') return <rect x={x - 10} y={y - 2} width={20} height={5} rx={2.5} fill="#2B1A15" />;
	if (state === 'hearts') {
		const s = 1.25 * pulse;
		return (
			<g transform={`translate(${x} ${y}) scale(${s})`}>
				<path d="M0,9 C-14,-1 -13,-12 -6,-12 C-2,-12 0,-9 0,-6 C0,-9 2,-12 6,-12 C13,-12 14,-1 0,9 Z" fill="#B82E5C" transform="translate(0 1.2) scale(1.12)" />
				<path d="M0,9 C-14,-1 -13,-12 -6,-12 C-2,-12 0,-9 0,-6 C0,-9 2,-12 6,-12 C13,-12 14,-1 0,9 Z" fill="#E8457C" />
				<ellipse cx={-5} cy={-6} rx={2.6} ry={2} fill="#FFC2D6" />
			</g>
		);
	}
	return (
		<g>
			<circle cx={x} cy={y} r={9.5} fill="#3B4A16" opacity={0.55} />
			<circle cx={x + lx} cy={y + ly} r={8.2} fill={c} />
			<circle cx={x + lx * 1.3} cy={y + ly * 1.3} r={4.2} fill="#141A08" />
			<circle cx={x + lx + 2.6} cy={y + ly - 2.8} r={2.4} fill="#FFFFFF" opacity={0.9} />
		</g>
	);
};

/** Tapered brow: thick at the inner end, thin at the outer end (side = -1 left brow, +1 right brow). */
const Brow: React.FC<{x: number; y: number; rot: number; c: string; side: number}> = ({x, y, rot, c, side}) => (
	<g transform={`translate(${x} ${y}) rotate(${rot}) scale(${side} 1)`}>
		<path d="M-17,1 Q-14,-6 -2,-7 Q10,-7.5 15,-4 Q17,1 13,4 Q2,3 -14,5 Q-18,4 -17,1 Z" fill={c} />
	</g>
);

const MouthShape: React.FC<{m: Mouth; x: number; y: number; onBeard: boolean}> = ({m, x, y, onBeard}) => {
	const dark = onBeard ? '#120F0D' : P.mouth;
	switch (m) {
		case 'open':
			return (
				<g>
					<rect x={x - 12} y={y - 9} width={24} height={20} rx={9} fill={dark} />
					<ellipse cx={x} cy={y + 6} rx={8} ry={4.5} fill={P.tongue} />
					<rect x={x - 9} y={y - 8} width={18} height={5} rx={2.5} fill="#FFFFFF" />
				</g>
			);
		case 'mid':
			return (
				<g>
					<rect x={x - 11} y={y - 5} width={22} height={11} rx={5.5} fill={dark} />
					<rect x={x - 8} y={y - 4} width={16} height={4} rx={2} fill="#FFFFFF" />
				</g>
			);
		case 'O':
			return (
				<g>
					<ellipse cx={x} cy={y + 1} rx={8.5} ry={11} fill={dark} />
					<path d={`M${x},${y - 6} Q${x + 5},${y + 2} ${x},${y + 5} Q${x - 5},${y + 2} ${x},${y - 6} Z`} fill="#FFFFFF" />
				</g>
			);
		case 'o':
			return <ellipse cx={x} cy={y + 1} rx={5.5} ry={7} fill={dark} />;
		case 'grin':
			return (
				<g>
					<rect x={x - 16} y={y - 7} width={32} height={15} rx={7} fill={dark} />
					<rect x={x - 13} y={y - 5} width={26} height={11} rx={5} fill="#FFFFFF" />
					<rect x={x - 13} y={y - 0.6} width={26} height={1.6} fill="#C9B8B0" />
				</g>
			);
		case 'yell':
			return (
				<g>
					<path d={`M${x - 16},${y - 10} Q${x},${y - 14} ${x + 16},${y - 10} Q${x + 18},${y + 16} ${x},${y + 18} Q${x - 18},${y + 16} ${x - 16},${y - 10} Z`} fill={dark} />
					<ellipse cx={x} cy={y + 11} rx={10} ry={5.5} fill={P.tongue} />
					<rect x={x - 12} y={y - 10} width={24} height={5} rx={2.5} fill="#FFFFFF" />
				</g>
			);
		case 'smile':
			return (
				<g>
					<path d={`M${x - 15},${y - 4} Q${x},${y + 14} ${x + 15},${y - 4} Q${x},${y + 4} ${x - 15},${y - 4} Z`} fill={dark} />
					<path d={`M${x - 11},${y - 1} Q${x},${y + 4} ${x + 11},${y - 1} L${x + 10},${y - 2.5} Q${x},${y + 1} ${x - 10},${y - 2.5} Z`} fill="#FFFFFF" />
				</g>
			);
		case 'flat':
			return <rect x={x - 11} y={y - 2} width={22} height={4.5} rx={2.2} fill={dark} />;
		default:
			return onBeard ? <rect x={x - 10} y={y - 2.2} width={20} height={4.4} rx={2.2} fill="#FFFFFF" opacity={0.85} /> : <rect x={x - 10} y={y - 2} width={20} height={4.5} rx={2.2} fill={dark} />;
	}
};

const BROW_ROT: Record<Brows, [number, number, number]> = {
	neutral: [-3, 3, 0],
	angry: [16, -16, 3],
	worried: [-16, 16, -2],
	happy: [-6, 6, -4],
	raised: [-4, 4, -8],
};

// v3 head kit: a rounded squircle face (soft jaw corners), a per-character hair mass under the helmet,
// the ear over the sideburn, and rounded beard silhouettes. Coordinates are before the 1.16 x widen.
const FACE = 'M-40,-98 Q-41,-136 -4,-136 L16,-136 Q53,-136 53,-98 L54,-46 Q55,4 14,5 L4,5 Q-39,4 -40,-38 Z';

function hairPaths(style: 'crop' | 'side' | 'swoop'): string[] {
	// [mass inside the face clip, optional extra tuft]
	const crop = 'M-46,-142 L58,-142 L58,-112 Q44,-106 30,-111 Q14,-104 -2,-110 Q-10,-108 -12,-98 L-13,-64 Q-14,-50 -22,-46 L-46,-46 Z';
	if (style === 'crop') return [crop];
	if (style === 'side') return [crop, 'M-6,-112 Q4,-90 26,-96 Q40,-100 44,-112 Q20,-104 -6,-112 Z'];
	return ['M-46,-142 L58,-142 L58,-120 Q36,-122 18,-104 Q2,-88 -10,-72 L-13,-58 Q-16,-48 -24,-46 L-46,-46 Z', 'M58,-120 Q40,-110 30,-96 Q22,-86 14,-84 Q22,-104 36,-118 Z'];
}

/** Head in its own frame: origin at the neck top, the face is ~135 tall above it. */
export const Head: React.FC<{look: Look; pose: Pose}> = ({look, pose}) => {
	const id = useId().replace(/:/g, '');
	const skin = look.skin ?? P.skin;
	const eyes = pose.eyes ?? 'open';
	const lx = pose.lookX ?? 1.2;
	const ly = pose.lookY ?? 0;
	const [br1, br2, bdy] = BROW_ROT[pose.brows ?? 'neutral'];
	const beard = look.beard;
	const bc = look.beardColor ?? look.hair;
	const mouth = pose.mouth ?? 'closed';
	const mx = 22;
	const my = beard === 'full' ? -18 : -22;
	const pulse = pose.heartPulse ?? 1;
	const hp = hairPaths(look.hairStyle ?? (look.hairFringe ? 'side' : 'crop'));
	return (
		<g>
			{/* hair mass at the back of the skull, behind the face, under the helmet rim */}
			<path d="M-36,-112 L-64,-108 Q-72,-80 -62,-56 Q-54,-44 -40,-46 Z" fill={look.hair} />
			{/* face (widened 16% about its centre line) */}
			<g transform="translate(6 0) scale(1.16 1) translate(-6 0)">
				<clipPath id={`face${id}`}>
					<path d={FACE} />
				</clipPath>
				<path d={FACE} fill={skin} />
				<g clipPath={`url(#face${id})`}>
					{/* shadow side (far cheek / under-jaw) */}
					<path d="M-40,-134 L-22,-134 Q-30,-70 -16,6 L-40,6 Z" fill={P.skinShade} />
					<path d="M-40,-14 Q8,-2 56,-14 L56,6 L-40,6 Z" fill={P.skinShade} opacity={0.6} />
					{/* hair mass under the helmet: top band, a block at the back down to the sideburn */}
					<path d={hp[0]} fill={look.hair} />
					{hp[1] && <path d={hp[1]} fill={look.hair} />}
					<path d="M-12,-98 L-13,-64 Q-14,-50 -22,-46 L-16,-46 Q-8,-52 -7,-66 L-6,-100 Z" fill="#000" opacity={0.18} />
					{/* rim light on the lit cheek */}
					<path d="M50,-104 Q55,-60 48,-12 L56,-12 L56,-104 Z" fill="#FFE2C8" opacity={0.35} />
					{beard === 'stubble' && <path d="M-22,-46 Q16,-34 56,-46 L56,6 L-22,6 Z" fill="#7A6050" opacity={0.28} />}
				</g>
				{/* cheeks */}
				<ellipse cx={-6} cy={-46} rx={10} ry={8} fill={P.blush} opacity={0.6} />
				<ellipse cx={46} cy={-46} rx={8} ry={8} fill={P.blush} opacity={0.6} />
				{/* nose */}
				<path d="M20,-80 Q18,-62 14,-54 Q22,-46 33,-51 Q31,-62 28,-80 Z" fill={P.skinDeep} opacity={0.85} />
				<ellipse cx={26} cy={-52} rx={6} ry={4} fill="#C98466" opacity={0.6} />
				{/* eyes + brows */}
				<Eye x={8} y={-74} c={look.eye} lx={lx} ly={ly} state={eyes} pulse={pulse} />
				<Eye x={38} y={-74} c={look.eye} lx={lx} ly={ly} state={eyes} pulse={pulse} />
				<Brow x={7} y={-93 + bdy} rot={br1} c={look.brow ?? (look.head === 'cap' ? '#3A2618' : '#2A1E15')} side={-1} />
				<Brow x={39} y={-93 + bdy} rot={br2} c={look.brow ?? (look.head === 'cap' ? '#3A2618' : '#2A1E15')} side={1} />
				{/* facial hair (rounded silhouettes) + mouth */}
				{beard === 'full' && (
					<g>
						<path d="M-36,-60 Q-26,-58 -20,-46 Q-10,-34 6,-38 Q24,-46 46,-40 Q54,-38 55,-42 L56,-12 Q58,24 18,24 L4,24 Q-38,22 -39,-22 Z" fill={bc} />
						<path d="M2,-40 Q24,-50 48,-41 Q50,-35 46,-33 Q24,-41 4,-33 Q0,-35 2,-40 Z" fill="#000" opacity={0.22} />
						<path d="M-34,-18 Q-30,18 2,20 L4,24 Q-38,22 -39,-22 Z" fill="#000" opacity={0.2} />
						<path d="M30,14 Q44,10 50,-4" stroke="#FFFFFF" strokeOpacity={0.12} strokeWidth={4} fill="none" strokeLinecap="round" />
					</g>
				)}
				{beard === 'goatee' && (
					<g>
						<path d="M2,-38 Q12,-46 23,-40 Q34,-46 44,-38 Q48,-32 44,-29 Q34,-34 23,-32 Q12,-34 2,-29 Q-2,-32 2,-38 Z" fill={bc} />
						<path d="M6,-26 Q23,-30 40,-26 Q46,-24 46,-14 L46,-4 Q44,22 23,24 Q2,22 0,-4 L0,-14 Q0,-24 6,-26 Z" fill={bc} />
						<path d="M1,-8 Q4,20 23,22 L23,17 Q8,15 6,-6 Z" fill="#000" opacity={0.18} />
					</g>
				)}
				{beard === 'moustache' && (
					<g>
						<path d="M-2,-36 Q8,-46 23,-40 Q38,-46 48,-36 Q52,-26 46,-24 Q36,-32 23,-30 Q10,-32 0,-24 Q-6,-26 -2,-36 Z" fill={bc} />
						<path d="M8,-36 Q16,-40 23,-37 Q30,-40 38,-36" stroke="#FFFFFF" strokeOpacity={0.14} strokeWidth={3} fill="none" strokeLinecap="round" />
					</g>
				)}
				<MouthShape m={mouth} x={mx + 1} y={beard === 'moustache' ? -16 : my} onBeard={beard === 'full' || beard === 'goatee'} />
			</g>
			{/* ear over the sideburn at the back edge, with an inner fold */}
			<ellipse cx={-48} cy={-62} rx={16} ry={23} fill={skin} />
			<ellipse cx={-48} cy={-62} rx={16} ry={23} fill={P.skinShade} opacity={0.45} />
			<path d="M-54,-74 Q-44,-84 -42,-66 Q-42,-52 -52,-50" fill="none" stroke={P.skinDeep} strokeWidth={5} strokeLinecap="round" />
			{pose.sweat && <path d="M58,-104 Q66,-90 64,-84 Q60,-78 55,-84 Q53,-90 58,-104 Z" fill="#BFE6FF" />}
			{/* headgear */}
			{look.head === 'helmet' ? <Helmet /> : <FieldCap />}
		</g>
	);
};

const Helmet: React.FC = () => (
	<g>
		<path d="M-62,-100 Q-66,-182 6,-186 Q78,-182 76,-100 Z" fill="url(#camoHelm)" />
		<path d="M30,-180 Q72,-170 76,-100 L60,-100 Q58,-160 30,-180 Z" fill="#000" opacity={0.14} />
		<path d="M-40,-160 Q-10,-182 22,-180 Q-8,-174 -32,-150 Z" fill="#FFFDE8" opacity={0.2} />
		<rect x={-66} y={-112} width={146} height={20} rx={10} fill="url(#camoHelm)" />
		<rect x={-66} y={-102} width={146} height={10} rx={5} fill="#000" opacity={0.2} />
		{/* goggles on the brim */}
		<path d="M-58,-136 Q6,-150 74,-132" fill="none" stroke={P.strap} strokeWidth={11} strokeLinecap="round" />
		<rect x={-16} y={-166} width={80} height={38} rx={15} fill="#262624" />
		<rect x={-12} y={-162} width={72} height={30} rx={12} fill={P.lens} />
		<rect x={-6} y={-158} width={58} height={8} rx={4} fill={P.lensHi} />
		<path d="M20,-132 Q24,-140 28,-132 Z" fill="#262624" />
	</g>
);

const FieldCap: React.FC = () => (
	<g>
		<path d="M-50,-104 Q-54,-160 -10,-168 L40,-170 Q66,-166 64,-104 Z" fill="url(#camoOff)" />
		<path d="M40,-170 Q66,-166 64,-104 L50,-104 Q52,-150 40,-170 Z" fill="#000" opacity={0.15} />
		<path d="M-20,-108 L84,-112 Q92,-104 84,-96 L-18,-94 Z" fill="#5C573C" />
		<path d="M-20,-108 L84,-112 Q88,-108 86,-104 L-18,-102 Z" fill="#7A7552" />
		<rect x={-50} y={-116} width={114} height={12} rx={4} fill="#625D40" />
	</g>
);

/** The full soldier puppet. */
export const Soldier: React.FC<{look: Look; pose: Pose; x: number; y: number; s?: number; shadow?: boolean}> = ({look, pose, x, y, s = 1, shadow = true}) => {
	const f = pose.facing ?? 1;
	const bob = pose.bob ?? 0;
	const crouch = pose.crouch ?? 0;
	const lean = pose.lean ?? 0;
	const breathe = pose.breathe ?? 0;
	const legsKind = pose.legs ?? 'stand';
	const camo = camoFill(look);
	const kneel = legsKind === 'kneel';
	const bw = look.build?.w ?? 1.12; // torso width factor (v2: bulkier than v1's 1.0)
	const belly = look.build?.belly ?? 0;
	const legW = 82 * (look.build?.leg ?? 1);
	const hipY = -250 + bob + crouch * 40 + (kneel ? 105 : 0);
	const torsoDY = hipY + 250; // torso offset
	// --- legs
	const legs: React.ReactNode[] = [];
	const boots: React.ReactNode[] = [];
	const ph = pose.legPhase ?? 0;
	const legDefs: {hip: [number, number]; foot: [number, number]; bootRot: number; far: boolean}[] = [];
	if (kneel) {
		legDefs.push({hip: [26, hipY], foot: [122, -48], bootRot: 0, far: true});
		legDefs.push({hip: [-24, hipY], foot: [-150, -40], bootRot: 42, far: false});
	} else {
		const sw = legsKind === 'march' ? 1 : 0;
		const liftF = Math.max(0, Math.sin(ph * Math.PI * 2)) * 34 * sw;
		const liftN = Math.max(0, -Math.sin(ph * Math.PI * 2)) * 34 * sw;
		const spread = crouch * 26 + (pose.stance ?? 0);
		legDefs.push({hip: [32, hipY], foot: [44 + spread + liftF * 0.5, -58 - liftF], bootRot: -liftF * 0.2, far: true});
		legDefs.push({hip: [-32, hipY], foot: [-40 - spread + liftN * 0.5, -58 - liftN], bootRot: -liftN * 0.2, far: false});
	}
	if (legsKind !== 'none')
		for (const L of legDefs) {
			const k = ik(L.hip, L.foot, 100, 100, -1);
			const d = `M${L.hip[0]},${L.hip[1]} L${k[0]},${k[1]} L${L.foot[0]},${L.foot[1]}`;
			// cargo pocket on the thigh, oriented along the thigh
			const ta = deg(Math.atan2(k[1] - L.hip[1], k[0] - L.hip[0]));
			const tm: [number, number] = [L.hip[0] + (k[0] - L.hip[0]) * 0.55, L.hip[1] + (k[1] - L.hip[1]) * 0.55];
			legs.push(
				<g key={`l${L.far}`}>
					<path d={d} fill="none" stroke={camo} strokeWidth={legW} strokeLinecap="round" strokeLinejoin="round" />
					{L.far && <path d={d} fill="none" stroke="#000" strokeOpacity={0.16} strokeWidth={legW} strokeLinecap="round" strokeLinejoin="round" />}
					{!L.far && (
						<g transform={`translate(${tm[0]} ${tm[1]}) rotate(${ta - 90})`}>
							<rect x={-30} y={-26} width={44} height={52} rx={9} fill={camoDark(look)} />
							<rect x={-30} y={-26} width={44} height={14} rx={6} fill="#000" opacity={0.18} />
						</g>
					)}
					{/* trouser cuff bunching over the boot */}
					<path d={`M${L.foot[0] - 38},${L.foot[1] - 12} Q${L.foot[0]},${L.foot[1] - 2} ${L.foot[0] + 38},${L.foot[1] - 12}`} stroke="#000" strokeOpacity={0.2} strokeWidth={10} strokeLinecap="round" fill="none" />
				</g>,
			);
			boots.push(<Boot key={`b${L.far}`} x={L.foot[0]} y={L.foot[1]} rot={L.bootRot} s={1.18} />);
		}
	// --- arms (torso frame)
	const shN: [number, number] = [-66 * bw, -430];
	const shF: [number, number] = [64 * bw, -430];
	const g = pose.gun ?? null;
	const resolve = (h: Hand | undefined, sh: [number, number], dir: number): [number, number] | null => {
		if (h === 'hidden') return null;
		if (h === 'grip' && g) return gunPt(g, 'grip');
		if (h === 'fore' && g) return gunPt(g, 'fore');
		if (Array.isArray(h)) return h;
		return [sh[0] + dir * 10, -262 + Math.sin(breathe * 6.28) * 2];
	};
	const hN = resolve(pose.handN, shN, -1);
	const hF = resolve(pose.handF, shF, 1);
	const arm = (sh: [number, number], h: [number, number], near: boolean) => {
		const bend = h[1] > sh[1] + 60 && Math.abs(h[0] - sh[0]) < 90 ? (near ? 1 : -1) : near ? -1 : 1;
		const e = ik(sh, h, 112, 104, bend);
		const ang = deg(Math.atan2(e[1] - sh[1], e[0] - sh[0]));
		const pm: [number, number] = [sh[0] + (e[0] - sh[0]) * 0.34, sh[1] + (e[1] - sh[1]) * 0.34];
		// the patch is sewn on the sleeve but kept near-upright so the stripes always read horizontal
		let pr = ang - 90;
		while (pr > 180) pr -= 360;
		while (pr < -180) pr += 360;
		pr = Math.max(-24, Math.min(24, pr));
		const d = `M${sh[0]},${sh[1]} L${e[0]},${e[1]} L${h[0]},${h[1]}`;
		return (
			<g>
				<path d={d} fill="none" stroke={camo} strokeWidth={62} strokeLinecap="round" strokeLinejoin="round" />
				<path d={`M${e[0]},${e[1]} L${h[0]},${h[1]}`} fill="none" stroke="#000" strokeOpacity={near ? 0.06 : 0.16} strokeWidth={62} strokeLinecap="round" />
				{/* sleeve cuff */}
				<circle cx={h[0] + (e[0] - h[0]) * 0.22} cy={h[1] + (e[1] - h[1]) * 0.22} r={27} fill="#000" opacity={0.12} />
				{near && look.patch !== 'none' && (
					<g transform={`translate(${pm[0]} ${pm[1]}) rotate(${pr}) scale(${f} 1)`}>
						<Flag kind={look.patch} x={-20} y={-14} w={40} h={27} r={4} />
					</g>
				)}
			</g>
		);
	};
	const handShape = (h: [number, number], point: boolean, near: boolean) => (
		<g transform={`translate(${h[0]} ${h[1]}) scale(${near ? pose.handNScale ?? 1 : 1})`}>
			{point && (
				<g transform={`rotate(${pose.pointAng ?? 0})`}>
					<rect x={14} y={-12} width={46} height={18} rx={9} fill={P.hand} />
					<rect x={14} y={-1} width={46} height={7} rx={3.5} fill={P.handShade} opacity={0.6} />
					<rect x={-2} y={6} width={26} height={20} rx={10} fill={P.handShade} />
				</g>
			)}
			<circle r={29} fill={P.hand} />
			<path d="M-27,8 Q-8,32 24,14 Q19,27 0,29 Q-21,28 -27,8 Z" fill={P.handShade} opacity={near ? 0.55 : 0.85} />
			<ellipse cx={-9} cy={-14} rx={9} ry={5.5} fill="#FFF0E2" opacity={0.35} />
		</g>
	);
	const carrier = pose.carrier !== false;
	const isOff = look.camo === 'off';
	const holding = !!g;
	return (
		<g transform={`translate(${x} ${y}) scale(${s * f} ${s})`}>
			{shadow && <ellipse cx={8} cy={4} rx={kneel ? 200 : 150} ry={19} fill="url(#softShadow)" />}
			{legs}
			{boots}
			<g transform={`rotate(${lean} 0 ${hipY}) translate(0 ${torsoDY})`}>
				<g transform={`translate(0 -250) scale(1 ${1 + Math.sin(breathe * 6.28) * 0.01}) translate(0 250)`}>
					{/* far arm behind the body when it hangs */}
					{hF && pose.handF === undefined && arm(shF, hF, false)}
					{hF && pose.handF === undefined && handShape(hF, false, false)}
					<g transform={`scale(${bw} 1)`}>
						{/* pelvis + belt */}
						<rect x={-74} y={-302} width={148} height={96} rx={30} fill={camo} />
						<rect x={-76} y={-302} width={152} height={24} rx={8} fill="#3B3A2A" />
						<rect x={-76} y={-302} width={152} height={5} rx={2.5} fill="#56553F" />
						<rect x={-12} y={-301} width={22} height={21} rx={4} fill="none" stroke={P.buckle} strokeWidth={4} />
						{/* torso: wide shoulders tapering slightly to the belt */}
						<path d="M-80,-286 L-86,-418 Q-88,-474 -36,-474 L36,-474 Q88,-474 86,-418 L80,-286 Z" fill={camo} />
						<path d="M52,-470 Q88,-464 86,-418 L80,-286 L58,-286 Z" fill="#000" opacity={0.13} />
						<path d="M-74,-462 Q-52,-474 -10,-474 Q-52,-466 -70,-444 Z" fill="#FFFDE8" opacity={0.16} />
						{belly > 0 && (
							<g>
								<path d={`M-40,-380 Q${70 + 26 * belly},-372 ${84 + 24 * belly},-330 Q${88 + 22 * belly},-292 50,-284 L-40,-284 Z`} fill={camo} />
								<path d={`M40,-372 Q${70 + 26 * belly},-366 ${84 + 24 * belly},-330 Q${88 + 22 * belly},-292 50,-284 L40,-284 Z`} fill="#000" opacity={0.14} />
							</g>
						)}
					</g>
					{/* neck */}
					{!pose.noHead && <rect x={-26} y={-490} width={58} height={34} rx={11} fill={P.skinShade} />}
					<g transform={`scale(${bw} 1)`}>
						{carrier && !isOff && (
							<g>
								<rect x={-70} y={-456} width={142} height={166} rx={16} fill={camoDark(look)} />
								<rect x={-70} y={-456} width={142} height={10} rx={5} fill="#FFFDE8" opacity={0.1} />
								<rect x={48} y={-456} width={24} height={166} rx={10} fill="#000" opacity={0.14} />
								<rect x={-64} y={-488} width={30} height={52} rx={8} fill={camoDark(look)} />
								<rect x={36} y={-488} width={30} height={52} rx={8} fill={camoDark(look)} />
								<rect x={-64} y={-450} width={30} height={20} rx={5} fill="none" stroke={P.buckle} strokeWidth={5} />
								<rect x={36} y={-450} width={30} height={20} rx={5} fill="none" stroke={P.buckle} strokeWidth={5} />
								<rect x={-28} y={-440} width={58} height={40} rx={7} fill="#3E3D29" />
								<rect x={-22} y={-434} width={46} height={10} rx={4} fill="#57553C" />
								{/* MOLLE webbing rows */}
								{[-392, -380].map((wy) => (
									<rect key={wy} x={-62} y={wy} width={126} height={4} rx={2} fill="#000" opacity={0.16} />
								))}
								{[-62, -16, 30].map((px) => (
									<g key={px}>
										<rect x={px} y={-364} width={42} height={68} rx={9} fill="#4E4B33" />
										<rect x={px} y={-364} width={42} height={21} rx={7} fill="#3A3926" />
										<rect x={px + 15} y={-352} width={12} height={10} rx={3} fill="#2B2A1C" />
										<rect x={px + 34} y={-358} width={8} height={60} rx={4} fill="#000" opacity={0.15} />
										<rect x={px + 3} y={-363} width={30} height={3} rx={1.5} fill="#6A684C" />
									</g>
								))}
							</g>
						)}
						{isOff && (
							<g>
								{/* officer: shirt pockets, shoulder boards, ribbons */}
								<rect x={-62} y={-434} width={44} height={38} rx={6} fill="#5E5940" />
								<rect x={20} y={-434} width={44} height={38} rx={6} fill="#5E5940" />
								<rect x={-62} y={-434} width={44} height={10} rx={4} fill="#4E4A33" />
								<rect x={20} y={-434} width={44} height={10} rx={4} fill="#4E4A33" />
								<rect x={-78} y={-474} width={48} height={18} rx={6} fill="#3E4A2E" />
								<rect x={32} y={-474} width={48} height={18} rx={6} fill="#3E4A2E" />
								{[-64, -50, 44, 58].map((sx) => (
									<path key={sx} transform={`translate(${sx} -465) scale(0.55)`} d="M0,-9 L2.6,-3 L9,-3 L4,1 L6,8 L0,4 L-6,8 L-4,1 L-9,-3 L-2.6,-3 Z" fill="#E8C34A" />
								))}
								<rect x={-60} y={-450} width={38} height={12} rx={2} fill="#2F6BC2" />
								<rect x={-60} y={-450} width={12} height={12} fill="#D9433A" />
								<rect x={-36} y={-450} width={12} height={12} fill="#F2C94C" />
								<rect x={22} y={-450} width={40} height={10} rx={2} fill="#E8E2D0" />
								<rect x={-5} y={-474} width={10} height={174} fill="#000" opacity={0.12} />
								{[-420, -380, -340].map((by) => (
									<circle key={by} cx={0} cy={by} r={5} fill="#3A3726" />
								))}
							</g>
						)}
					</g>
					{/* head */}
					{!pose.noHead && (
						<g transform={`translate(${4 + (pose.headX ?? 0)} ${-474 + (pose.headY ?? 0)}) rotate(${pose.headRot ?? 0})`}>
							<Head look={look} pose={pose} />
						</g>
					)}
					{/* arms, gun, hands. With a gun, the support (far) hand sits behind the rifle and the
					    near hand wraps the pistol grip below the receiver, so the gun's silhouette stays readable. */}
					{hF && pose.handF !== undefined && arm(shF, hF, false)}
					{hF && pose.handF !== undefined && holding && handShape(hF, !!pose.pointF, false)}
					{hN && arm(shN, hN, true)}
					{g && <Gun g={g} />}
					{hF && pose.handF !== undefined && !holding && handShape(hF, !!pose.pointF, false)}
					{hN && handShape(hN, !!pose.pointN, true)}
					{/* v3 grip wrap: the near hand's thumb lies along the receiver and the support hand's
					    fingertips curl round the handguard, so hands read as holding rather than floating */}
					{g && pose.handN === 'grip' && (
						<g transform={`translate(${g.x} ${g.y}) rotate(${g.rot}) scale(${g.s ?? 1})`}>
							<path d={`M${ANCH_GRIP[g.kind][0] - 14},${ANCH_GRIP[g.kind][1] - 30} L${ANCH_GRIP[g.kind][0] + 30},${ANCH_GRIP[g.kind][1] - 40}`} stroke={P.hand} strokeWidth={17} strokeLinecap="round" />
							<path d={`M${ANCH_GRIP[g.kind][0] - 12},${ANCH_GRIP[g.kind][1] - 25} L${ANCH_GRIP[g.kind][0] + 28},${ANCH_GRIP[g.kind][1] - 34}`} stroke={P.handShade} strokeWidth={5} strokeLinecap="round" opacity={0.7} />
							<path d={`M${ANCH_GRIP[g.kind][0] + 12},${ANCH_GRIP[g.kind][1] - 12} Q${ANCH_GRIP[g.kind][0] + 22},${ANCH_GRIP[g.kind][1]} ${ANCH_GRIP[g.kind][0] + 14},${ANCH_GRIP[g.kind][1] + 14}`} stroke={P.handShade} strokeWidth={4} fill="none" strokeLinecap="round" />
						</g>
					)}
					{g && pose.handF === 'fore' && (
						<g transform={`translate(${g.x} ${g.y}) rotate(${g.rot}) scale(${g.s ?? 1})`}>
							{[-14, 0, 14].map((dx, i) => (
								<g key={dx}>
									<circle cx={ANCH_FORE[g.kind][0] + dx} cy={ANCH_FORE[g.kind][1] + 6 - (i === 1 ? 2 : 0)} r={10} fill={P.hand} />
									<circle cx={ANCH_FORE[g.kind][0] + dx + 2} cy={ANCH_FORE[g.kind][1] + 9} r={6} fill={P.handShade} opacity={0.6} />
								</g>
							))}
						</g>
					)}
				</g>
			</g>
		</g>
	);
};
