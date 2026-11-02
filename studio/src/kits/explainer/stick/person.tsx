/**
 * stick/Person: a round-head story character (our own design for the story lane).
 *
 * Big bone-white head with one flat shadow crescent (light from the upper left), dot eyes, short bar brows, a small
 * nose bump, indigo line limbs, a costume torso and a period hat or wig. No outlines (house style A). Faces right;
 * use the layer's flipX to face left. Draws in a 600 x 700 box, feet on the bottom edge (seated: on a chair line).
 *
 * props
 *   costume   kempelen | empress | courtier | courtier2 | count | franklin | napoleon | master | plain
 *   face      neutral | smile | grin | smug | laugh | shock | worried | frown | angry | focus | sleepy
 *             (constant or [{t, v}] held from t)
 *   pose      stand | point | hold | holdHigh | armsUp | laugh | shrug | push | reach | handIn | wind | hips | sweep
 *             (constant or [{t, v}]; poses blend over 0.22 s)
 *   seated    true: legs bent forward, on a chair (chair: false for none)
 *   crouch    0..1 track: folds the body down (the hidden chess master)
 *   walk      0..1 track: leg swing + bob
 *   talk      [[t0, t1], ...] mouth flaps inside the windows
 *   look      -1..1 track: eyes left/right
 *   item      none | candle | key | piece  (in the front hand)
 *   seed      blink phase
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {num, str, track, clamp, lerp, easeInOut} from '../util';
import {c, K, f, hash, inWin, inkG, step, stepBlend} from './common';

type P2 = [number, number];
type Costume = {
	coat: string;
	coatShade: string;
	vest?: string;
	cravat?: string;
	legs: string;
	shoes: string;
	hat?: 'tricorn' | 'bicorne' | 'crown' | 'furcap' | 'none';
	hair?: 'wig' | 'wigTall' | 'updo' | 'side' | 'short' | 'messy' | 'none';
	hairColor?: string;
	gown?: string;
	gownShade?: string;
	glasses?: boolean;
	epaulettes?: boolean;
	buttons?: boolean;
};

const COSTUMES: Record<string, Costume> = {
	kempelen: {coat: c('violet-1'), coatShade: c('violet-0'), vest: c('amber-4'), cravat: c('bone-2'), legs: K.ink,
		shoes: c('ink-0'), hat: 'tricorn', hair: 'wig', hairColor: c('bone-0'), buttons: true},
	empress: {coat: c('magenta-2'), coatShade: c('magenta-1'), cravat: c('bone-2'), legs: K.ink, shoes: c('ink-0'),
		hat: 'crown', hair: 'updo', hairColor: c('bone-0'), gown: c('magenta-1'), gownShade: c('magenta-0')},
	courtier: {coat: c('tide-0'), coatShade: c('dusk-1'), vest: c('bone-1'), cravat: c('bone-2'), legs: c('bone-0'),
		shoes: c('ink-0'), hair: 'wig', hairColor: c('bone-0'), buttons: true},
	courtier2: {coat: c('kelp-1'), coatShade: c('kelp-0'), vest: c('magenta-3'), cravat: c('bone-2'), legs: c('bone-0'),
		shoes: c('ink-0'), hair: 'wigTall', hairColor: c('bone-0'), buttons: true},
	count: {coat: c('amber-1'), coatShade: c('amber-0'), vest: c('amber-4'), cravat: c('bone-2'), legs: c('bone-0'),
		shoes: c('ink-0'), hair: 'wig', hairColor: c('bone-0'), buttons: true},
	franklin: {coat: c('ochre-0'), coatShade: c('amber-0'), vest: c('ochre-2'), cravat: c('bone-2'), legs: K.ink,
		shoes: c('ink-0'), hat: 'furcap', hair: 'side', hairColor: c('bone-0'), glasses: true},
	napoleon: {coat: c('dusk-1'), coatShade: c('ink-1'), vest: c('bone-1'), cravat: c('bone-2'), legs: c('bone-1'),
		shoes: c('ink-0'), hat: 'bicorne', hair: 'short', hairColor: c('ink-1'), epaulettes: true, buttons: true},
	master: {coat: c('sky-1'), coatShade: c('sky-0'), legs: K.ink, shoes: c('ink-0'), hair: 'messy', hairColor: c('ink-1')},
	plain: {coat: c('coral-2'), coatShade: c('coral-0'), legs: K.ink, shoes: c('ink-0'), hair: 'short', hairColor: c('ink-1')},
};

// ------------------------------------------------------------------ geometry (600 x 700 box)
const HEAD: P2 = [300, 150];
const HR = 118;
const SH_L: P2 = [242, 292];
const SH_R: P2 = [358, 292];
const HIP_L: P2 = [268, 470];
const HIP_R: P2 = [332, 470];
const UPPER = 98;
const LOWER = 92;
const LIMB = 24;

// hand targets per pose [left, right] (left = the far arm)
const POSES: Record<string, [P2, P2]> = {
	stand: [[214, 478], [386, 478]],
	point: [[214, 478], [540, 240]],
	hold: [[214, 478], [440, 352]],
	holdHigh: [[214, 478], [452, 236]],
	armsUp: [[178, 110], [422, 110]],
	laugh: [[268, 418], [336, 420]],
	shrug: [[150, 286], [450, 286]],
	push: [[452, 372], [480, 352]],
	reach: [[214, 478], [520, 420]],
	handIn: [[214, 478], [312, 352]],
	wind: [[214, 478], [476, 404]],
	hips: [[226, 442], [374, 442]],
	sweep: [[214, 478], [548, 330]],
};

function ik(s: P2, t: P2, a: number, b: number, out: number): P2 {
	const dx = t[0] - s[0];
	const dy = t[1] - s[1];
	const d = clamp(Math.hypot(dx, dy), Math.abs(a - b) + 1, a + b - 1);
	const base = Math.atan2(dy, dx);
	const cosA = (a * a + d * d - b * b) / (2 * a * d);
	const A = Math.acos(clamp(cosA, -1, 1));
	const e1: P2 = [s[0] + a * Math.cos(base + A), s[1] + a * Math.sin(base + A)];
	const e2: P2 = [s[0] + a * Math.cos(base - A), s[1] + a * Math.sin(base - A)];
	// elbow away from the body's centre line, and down when it is a near tie
	const score = (e: P2) => out * (e[0] - 300) + 0.35 * e[1];
	return score(e1) >= score(e2) ? e1 : e2;
}

const lerp2 = (a: P2, b: P2, t: number): P2 => [lerp(a[0], b[0], t), lerp(a[1], b[1], t)];

// ------------------------------------------------------------------ faces
type Face = {eyes: string; brow: [number, number]; browY: number; mouth: string; sweat?: boolean};
const FACES: Record<string, Face> = {
	neutral: {eyes: 'dot', brow: [0, 0], browY: 0, mouth: 'smallSmile'},
	smile: {eyes: 'dot', brow: [-6, 6], browY: -6, mouth: 'smile'},
	grin: {eyes: 'dot', brow: [-8, 8], browY: -8, mouth: 'grin'},
	smug: {eyes: 'half', brow: [10, -4], browY: 4, mouth: 'smirk'},
	laugh: {eyes: 'happy', brow: [-10, 10], browY: -10, mouth: 'laugh'},
	shock: {eyes: 'wide', brow: [-12, 12], browY: -18, mouth: 'o'},
	worried: {eyes: 'dot', brow: [-16, 16], browY: -6, mouth: 'wavy', sweat: true},
	frown: {eyes: 'dot', brow: [16, -16], browY: 4, mouth: 'frown'},
	angry: {eyes: 'squint', brow: [24, -24], browY: 8, mouth: 'teeth'},
	focus: {eyes: 'dot', brow: [8, -8], browY: 8, mouth: 'flat'},
	sleepy: {eyes: 'closed', brow: [0, 0], browY: 2, mouth: 'flat'},
};

function Eyes({face, look, blink}: {face: Face; look: number; blink: boolean}) {
	const xs = [322, 378].map((x) => x + look * 12);
	const y = 148;
	const kind = blink && (face.eyes === 'dot' || face.eyes === 'wide' || face.eyes === 'half') ? 'closed' : face.eyes;
	return (
		<g>
			{xs.map((x, i) => {
				if (kind === 'dot') return <ellipse key={i} cx={x} cy={y} rx={10} ry={14} fill={K.ink} />;
				if (kind === 'wide')
					return (
						<g key={i}>
							<circle cx={x} cy={y} r={21} fill={c('bone-2')} />
							<circle cx={x + 3} cy={y} r={8} fill={K.ink} />
						</g>
					);
				if (kind === 'half')
					return (
						<g key={i}>
							<ellipse cx={x} cy={y + 3} rx={10} ry={10} fill={K.ink} />
							<rect x={x - 14} y={y - 12} width={28} height={11} rx={4} fill={K.skin} />
							<rect x={x - 13} y={y - 3} width={26} height={5} rx={2.5} fill={K.ink} />
						</g>
					);
				if (kind === 'squint')
					return <rect key={i} x={x - 12} y={y - 3} width={24} height={7} rx={3.5} fill={K.ink} />;
				if (kind === 'happy')
					return (
						<path key={i} d={`M ${x - 13} ${y + 5} Q ${x} ${y - 13} ${x + 13} ${y + 5}`} stroke={K.ink}
							strokeWidth={7} strokeLinecap="round" fill="none" />
					);
				// closed
				return (
					<path key={i} d={`M ${x - 12} ${y} Q ${x} ${y + 8} ${x + 12} ${y}`} stroke={K.ink} strokeWidth={6}
						strokeLinecap="round" fill="none" />
				);
			})}
		</g>
	);
}

function Brows({face, look}: {face: Face; look: number}) {
	const xs = [322, 378].map((x) => x + look * 10);
	const y = 110 + face.browY;
	return (
		<g>
			{xs.map((x, i) => (
				<rect key={i} x={x - 15} y={y - 4} width={30} height={9} rx={4.5} fill={K.ink}
					transform={`rotate(${i === 0 ? face.brow[0] : face.brow[1]} ${x} ${y})`} />
			))}
		</g>
	);
}

function Mouth({kind, open}: {kind: string; open: number}) {
	const x = 352;
	const y = 204;
	if (open > 0.5) {
		return (
			<g>
				<ellipse cx={x} cy={y + 2} rx={17} ry={14} fill={c('ink-0')} />
				<ellipse cx={x + 2} cy={y + 10} rx={10} ry={5} fill={c('coral-3')} />
			</g>
		);
	}
	switch (kind) {
		case 'smile':
			return <path d={`M ${x - 24} ${y - 4} Q ${x} ${y + 18} ${x + 24} ${y - 6}`} stroke={K.ink} strokeWidth={7} strokeLinecap="round" fill="none" />;
		case 'smallSmile':
			return <path d={`M ${x - 15} ${y - 2} Q ${x} ${y + 9} ${x + 15} ${y - 3}`} stroke={K.ink} strokeWidth={6.5} strokeLinecap="round" fill="none" />;
		case 'grin':
			return (
				<g>
					<path d={`M ${x - 32} ${y - 10} Q ${x} ${y + 34} ${x + 32} ${y - 12} Z`} fill={c('ink-0')} />
					<path d={`M ${x - 26} ${y - 8} L ${x + 26} ${y - 10} L ${x + 22} ${y - 2} L ${x - 22} ${y} Z`} fill={c('bone-2')} />
				</g>
			);
		case 'laugh':
			return (
				<g>
					<path d={`M ${x - 30} ${y - 12} Q ${x} ${y + 44} ${x + 32} ${y - 12} Z`} fill={c('ink-0')} />
					<ellipse cx={x + 2} cy={y + 14} rx={14} ry={7} fill={c('coral-3')} />
				</g>
			);
		case 'smirk':
			return <path d={`M ${x - 20} ${y + 2} Q ${x + 6} ${y + 8} ${x + 24} ${y - 10}`} stroke={K.ink} strokeWidth={7} strokeLinecap="round" fill="none" />;
		case 'o':
			return <ellipse cx={x} cy={y + 4} rx={12} ry={17} fill={c('ink-0')} />;
		case 'wavy':
			return <path d={`M ${x - 22} ${y + 2} q 7 -8 14 0 t 14 0 t 14 0`} stroke={K.ink} strokeWidth={6} strokeLinecap="round" fill="none" />;
		case 'frown':
			return <path d={`M ${x - 22} ${y + 8} Q ${x} ${y - 10} ${x + 22} ${y + 8}`} stroke={K.ink} strokeWidth={7} strokeLinecap="round" fill="none" />;
		case 'teeth':
			return (
				<g>
					<rect x={x - 26} y={y - 8} width={52} height={22} rx={6} fill={c('ink-0')} />
					<rect x={x - 22} y={y - 4} width={44} height={14} rx={3} fill={c('bone-2')} />
					<path d={`M ${x - 22} ${y + 3} H ${x + 22} M ${x - 8} ${y - 4} V ${y + 10} M ${x + 7} ${y - 4} V ${y + 10}`} stroke={c('bone-0')} strokeWidth={2.5} />
				</g>
			);
		default:
			return <rect x={x - 16} y={y - 3} width={32} height={7} rx={3.5} fill={K.ink} />;
	}
}

// ------------------------------------------------------------------ hats and hair
function Hair({kind, color, back}: {kind?: string; color: string; back: boolean}) {
	const sh = c('bone-0') === color ? c('sky-3') : c('ink-0');
	if (kind === 'wig' || kind === 'wigTall') {
		if (back)
			return (
				<g>
					<path d="M 200 120 Q 190 230 236 252 L 214 268 Q 168 220 182 140 Z" fill={color} />
					<rect x={182} y={178} width={18} height={70} rx={9} fill={c('ink-1')} transform="rotate(14 190 210)" />
				</g>
			);
		return (
			<g>
				{kind === 'wigTall' && <ellipse cx={292} cy={36} rx={92} ry={58} fill={color} />}
				<path d="M 186 132 Q 196 30 300 28 Q 394 30 412 104 Q 352 66 282 76 Q 222 88 212 150 Z" fill={color} />
				<circle cx={214} cy={160} r={26} fill={color} />
				<circle cx={214} cy={210} r={26} fill={color} />
				<path d="M 196 174 Q 214 186 236 172" stroke={sh} strokeWidth={5} fill="none" opacity={0.55} strokeLinecap="round" />
				<path d="M 196 224 Q 214 236 236 222" stroke={sh} strokeWidth={5} fill="none" opacity={0.55} strokeLinecap="round" />
			</g>
		);
	}
	if (kind === 'updo') {
		if (back) return null;
		return (
			<g>
				<ellipse cx={290} cy={20} rx={70} ry={52} fill={color} />
				<path d="M 186 140 Q 190 40 300 34 Q 404 40 414 120 Q 352 76 290 80 Q 226 86 206 150 Z" fill={color} />
				<path d="M 238 6 Q 290 -14 340 10" stroke={sh} strokeWidth={6} fill="none" opacity={0.5} strokeLinecap="round" />
			</g>
		);
	}
	if (kind === 'side') {
		if (back) return <path d="M 196 120 Q 176 236 236 270 L 250 250 Q 214 200 222 130 Z" fill={color} />;
		return <path d="M 190 120 Q 190 200 226 236 Q 214 170 232 120 Z" fill={color} />;
	}
	if (kind === 'short') {
		if (back) return null;
		return <path d="M 188 136 Q 196 36 304 32 Q 404 38 414 112 Q 360 70 300 82 Q 270 60 240 92 Q 214 104 206 150 Z" fill={color} />;
	}
	if (kind === 'messy') {
		if (back) return null;
		return (
			<path d="M 184 140 L 178 92 L 210 104 L 214 56 L 246 82 L 270 34 L 296 72 L 328 30 L 344 74 L 384 46 L 382 92 L 420 92 L 404 120 Q 340 84 280 94 Q 226 104 206 158 Z"
				fill={color} />
		);
	}
	return null;
}

function Hat({kind}: {kind?: string}) {
	if (kind === 'tricorn')
		return (
			<g>
				<path d="M 160 78 Q 300 120 450 70 Q 420 4 300 -6 Q 186 2 160 78 Z" fill={c('ink-1')} />
				<path d="M 160 78 Q 300 120 450 70 L 444 84 Q 300 136 166 92 Z" fill={c('amber-3')} />
				<path d="M 300 -6 Q 360 0 410 30 Q 352 20 300 22 Z" fill={c('ink-0')} />
			</g>
		);
	if (kind === 'bicorne')
		return (
			<g>
				<path d="M 128 76 Q 300 120 470 74 Q 420 -36 300 -40 Q 176 -36 128 76 Z" fill={c('ink-1')} />
				<path d="M 300 -40 Q 400 -30 452 40 Q 380 8 300 6 Z" fill={c('ink-0')} />
				<circle cx={384} cy={40} r={20} fill={c('tide-0')} />
				<circle cx={384} cy={40} r={13} fill={c('bone-2')} />
				<circle cx={384} cy={40} r={6} fill={c('coral-2')} />
			</g>
		);
	if (kind === 'crown')
		return (
			<g>
				<path d="M 238 44 L 252 -4 L 276 26 L 300 -14 L 324 26 L 348 -4 L 362 44 Z" fill={K.gold} />
				<path d="M 300 -14 L 324 26 L 348 -4 L 362 44 L 316 44 Z" fill={K.goldShade} />
				<circle cx={300} cy={28} r={7} fill={c('coral-2')} />
			</g>
		);
	if (kind === 'furcap')
		return (
			<g>
				<path d="M 196 96 Q 186 40 214 20 Q 226 -10 262 -6 Q 290 -24 320 -8 Q 356 -16 378 14 Q 414 34 404 96 Z" fill={c('amber-0')} />
				<path d="M 330 -8 Q 356 -16 378 14 Q 414 34 404 96 L 350 96 Q 362 40 330 -8 Z" fill={c('ochre-0')} />
				{[200, 236, 272, 308, 344, 380].map((x) => <circle key={x} cx={x + 10} cy={96} r={22} fill={c('ochre-0')} />)}
			</g>
		);
	return null;
}

// ------------------------------------------------------------------ props in hand
function Item({kind, at, t}: {kind: string; at: P2; t: number}) {
	const [x, y] = at;
	if (kind === 'candle') {
		const fl = 1 + 0.12 * Math.sin(t * 19) + 0.06 * Math.sin(t * 31);
		return (
			<g transform={`translate(${x} ${y}) scale(1.45) translate(${-x} ${-y})`} stroke="none">
				<circle cx={x} cy={y - 74} r={46 * fl} fill={c('amber-4')} opacity={0.22} stroke="none" />
				<rect x={x - 24} y={y - 6} width={48} height={12} rx={6} fill={K.gold} />
				<rect x={x - 11} y={y - 56} width={22} height={52} rx={5} fill={c('bone-2')} />
				<rect x={x + 1} y={y - 56} width={10} height={52} rx={4} fill={c('bone-0')} />
				<path d={`M ${x} ${y - 98 * fl + 4} Q ${x + 13} ${y - 70} ${x} ${y - 58} Q ${x - 13} ${y - 70} ${x} ${y - 98 * fl + 4} Z`} fill={c('amber-3')} />
				<path d={`M ${x} ${y - 82} Q ${x + 6} ${y - 68} ${x} ${y - 61} Q ${x - 6} ${y - 68} ${x} ${y - 82} Z`} fill={c('bone-2')} />
			</g>
		);
	}
	if (kind === 'key') {
		return (
			<g transform={`rotate(${(t * 220) % 360} ${x} ${y})`}>
				<rect x={x - 6} y={y - 40} width={12} height={46} rx={5} fill={K.gold} />
				<ellipse cx={x} cy={y - 44} rx={22} ry={13} fill={K.gold} />
				<ellipse cx={x} cy={y - 44} rx={10} ry={5} fill={K.goldShade} />
			</g>
		);
	}
	if (kind === 'piece') {
		return (
			<g>
				<path d={`M ${x - 18} ${y + 4} L ${x + 18} ${y + 4} L ${x + 12} ${y - 22} Q ${x} ${y - 30} ${x - 12} ${y - 22} Z`} fill={c('bone-2')} />
				<circle cx={x} cy={y - 34} r={11} fill={c('bone-2')} />
			</g>
		);
	}
	return null;
}

// ------------------------------------------------------------------ body
function arm(sh: P2, hand: P2, out: number) {
	const el = ik(sh, hand, UPPER, LOWER, out);
	return `M ${f(sh[0])} ${f(sh[1])} L ${f(el[0])} ${f(el[1])} L ${f(hand[0])} ${f(hand[1])}`;
}

export const Person: React.FC<KitComponentProps> = ({props, time}) => (
	<svg viewBox="0 0 600 700" width="100%" height="100%" preserveAspectRatio="xMidYMax meet" style={{overflow: 'visible'}}>
		<g {...inkG(props.ink)}>
			<PersonBody props={props} t={time} />
		</g>
	</svg>
);

/** the figure as an SVG group in the 600 x 700 box (for embedding in other drawings) */
export const PersonBody: React.FC<{props: Record<string, unknown>; t: number}> = ({props, t}) => {
	const cos = COSTUMES[str(props.costume, 'plain')] ?? COSTUMES.plain;
	const faceName = step<string>(props.face, t, 'neutral');
	const face = FACES[faceName] ?? FACES.neutral;
	const pb = stepBlend<string>(props.pose, t, 'stand');
	const blend = easeInOut(clamp(pb.since / 0.22));
	const P0 = POSES[pb.prev] ?? POSES.stand;
	const P1 = POSES[pb.cur] ?? POSES.stand;
	let hl = lerp2(P0[0], P1[0], blend);
	let hr = lerp2(P0[1], P1[1], blend);
	const seed = num(props.seed, 1);
	const seated = props.seated === true;
	const crouch = clamp(track(props.crouch, t, 0));
	const walk = clamp(track(props.walk, t, 0));
	const look = track(props.look, t, 0);
	const item = step<string>(props.item, t, 'none');
	// idle: breathing, laugh bounce, walk bob
	const laughing = faceName === 'laugh';
	const bob = Math.sin(t * 2.2 + seed) * 3 + (laughing ? Math.abs(Math.sin(t * 13)) * -10 : 0) +
		walk * Math.abs(Math.sin(t * 9)) * -12;
	const lean = (laughing ? Math.sin(t * 6.5) * 2.5 : 0) + crouch * 8;
	if (pb.cur === 'wind') hr = [hr[0] + Math.cos(t * 7) * 14, hr[1] + Math.sin(t * 7) * 14];
	if (laughing && pb.cur === 'laugh') {
		hl = [hl[0], hl[1] + Math.sin(t * 13) * 4];
		hr = [hr[0], hr[1] + Math.sin(t * 13) * 4];
	}
	// blink: every ~3.5 s for 0.12 s
	const per = 3.2 + hash(seed) * 1.6;
	const ph = (t + hash(seed + 3) * per) % per;
	const blink = ph < 0.12;
	const talking = inWin(props.talk, t);
	const open = talking ? (Math.sin(t * 26) > 0 ? 1 : 0) : 0;
	const isGown = !!cos.gown;

	// legs
	let legs: [P2, P2, P2][] = [];
	if (seated) {
		legs = [
			[HIP_L, [392, 486], [398, 672]],
			[HIP_R, [430, 478], [440, 672]],
		];
	} else {
		const sw = walk * Math.sin(t * 9) * 0.38;
		const kn = (hip: P2, a: number): [P2, P2, P2] => {
			const foot: P2 = [hip[0] + Math.sin(a) * 210, hip[1] + Math.cos(a) * 210];
			const knee: P2 = [(hip[0] + foot[0]) / 2 + Math.abs(a) * 20, (hip[1] + foot[1]) / 2];
			return [hip, knee, foot];
		};
		legs = [kn([HIP_L[0] - 6, HIP_L[1]], -0.08 + sw), kn([HIP_R[0] + 6, HIP_R[1]], 0.08 - sw)];
	}
	const bodyY = bob + crouch * 120;

	return (
		<g>
			{/* chair behind a seated figure */}
			{seated && props.chair !== false && (
				<g>
					<rect x={150} y={250} width={40} height={250} rx={12} fill={c('coral-0')} />
					<rect x={160} y={262} width={20} height={200} rx={8} fill={c('coral-1')} />
					<rect x={150} y={486} width={300} height={34} rx={10} fill={c('amber-0')} />
					<rect x={150} y={486} width={300} height={14} rx={7} fill={c('coral-1')} />
					<rect x={168} y={516} width={20} height={174} fill={c('amber-0')} />
					<rect x={412} y={516} width={20} height={174} fill={c('amber-0')} />
				</g>
			)}
			{/* ground shadow */}
			{!seated && <ellipse cx={300} cy={688} rx={150} ry={14} fill={c('ink-1')} opacity={0.22} stroke="none" />}
			{/* legs */}
			{!isGown &&
				legs.map(([h, k, ft], i) => (
					<g key={i}>
						<path d={`M ${f(h[0])} ${f(h[1] + bodyY * 0.4)} L ${f(k[0])} ${f(k[1] + crouch * 60)} L ${f(ft[0])} ${f(ft[1])}`}
							stroke={cos.legs} strokeWidth={LIMB + 4} strokeLinecap="round" strokeLinejoin="round" fill="none" />
						<ellipse cx={ft[0] + 16} cy={ft[1] + 2} rx={34} ry={16} fill={cos.shoes} />
					</g>
				))}
			<g transform={`translate(0 ${f(bodyY)}) rotate(${f(lean)} 300 470)`}>
				{/* back hair, back arm */}
				<Hair kind={cos.hair} color={cos.hairColor ?? K.ink} back />
				<path d={arm(SH_L, hl, -1)} stroke={cos.coatShade} strokeWidth={LIMB} strokeLinecap="round" strokeLinejoin="round" fill="none" />
				<circle cx={hl[0]} cy={hl[1]} r={17} fill={K.skinShade} />
				{/* gown */}
				{isGown && (
					<g>
						<path d={`M 236 404 Q 150 560 110 ${700 - bodyY} L 490 ${700 - bodyY} Q 450 560 364 404 Z`} fill={cos.gown} />
						<path d={`M 320 404 Q 380 540 410 ${700 - bodyY} L 490 ${700 - bodyY} Q 450 560 364 404 Z`} fill={cos.gownShade} />
						<path d={`M 160 ${640 - bodyY} Q 300 ${676 - bodyY} 450 ${640 - bodyY}`} stroke={c('bone-2')} strokeWidth={14} fill="none" strokeLinecap="round" opacity={0.9} />
					</g>
				)}
				{/* torso */}
				<path d="M 236 262 Q 300 246 364 262 L 398 470 Q 300 490 202 470 Z" fill={cos.coat} />
				<path d="M 300 254 Q 336 252 364 262 L 398 470 Q 350 482 318 484 Z" fill={cos.coatShade} />
				{cos.vest && <path d="M 284 262 L 316 262 L 322 452 L 278 452 Z" fill={cos.vest} />}
				{cos.buttons && [300, 340, 380, 420].map((y) => <circle key={y} cx={300} cy={y} r={5.5} fill={K.goldShade} />)}
				{cos.epaulettes && (
					<g>
						<rect x={214} y={262} width={50} height={20} rx={10} fill={K.gold} />
						<rect x={336} y={262} width={50} height={20} rx={10} fill={K.goldShade} />
					</g>
				)}
				{cos.cravat && <path d="M 270 258 Q 300 300 330 258 Q 300 252 270 258 Z" fill={cos.cravat} />}
				{/* head */}
				<g>
					<circle cx={HEAD[0]} cy={HEAD[1]} r={HR} fill={K.skinShade} />
					<circle cx={HEAD[0] - 9} cy={HEAD[1] - 9} r={HR - 8} fill={K.skin} />
					<circle cx={402 + look * 6} cy={176} r={13} fill={K.skinShade} />
					<circle cx={296} cy={186} r={13} fill={K.cheek} opacity={0.55} stroke="none" />
					<Hair kind={cos.hair} color={cos.hairColor ?? K.ink} back={false} />
					<g transform="translate(350 168) scale(1.32) translate(-350 -168)">
					<Brows face={face} look={look} />
					<Eyes face={face} look={look} blink={blink} />
					{cos.glasses && (
						<g fill="none" stroke={c('ink-1')} strokeWidth={5}>
							<circle cx={322 + look * 12} cy={148} r={24} />
							<circle cx={378 + look * 12} cy={148} r={24} />
							<path d={`M ${346 + look * 12} 146 H ${354 + look * 12}`} />
						</g>
					)}
					<Mouth kind={face.mouth} open={open} />
					</g>
					{face.sweat && (
						<path d="M 214 92 Q 226 116 214 128 Q 202 116 214 92 Z" fill={c('sky-2')}
							transform={`translate(0 ${f(((t * 30) % 30))})`} />
					)}
					<Hat kind={cos.hat} />
				</g>
				{/* front arm + item */}
				<path d={arm(SH_R, hr, 1)} stroke={cos.coat} strokeWidth={LIMB} strokeLinecap="round" strokeLinejoin="round" fill="none" />
				<circle cx={hr[0]} cy={hr[1]} r={17} fill={K.skin} />
				{item !== 'none' && <Item kind={item} at={[hr[0], hr[1] - 6]} t={t} />}
			</g>
		</g>
	);
};
