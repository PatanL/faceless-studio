// Two original 2D puppet characters for horror chat stories, waist-up, with swappable
// expressions, automatic blinking, mouth flap while talking, poses and lighting.
//   horror/Protagonist  - "Nora": young tenant, dark bob with a ragged fringe, olive hoodie.
//   horror/Neighbour    - "Mr. Hale": gaunt older neighbour, grey comb-over, pencil moustache,
//                         maroon cardigan. Doubles as the stranger / impostor.
// Art box is 500x760 (head ~ top 55%); size the layer at that ratio, e.g. 640x973.
import React from 'react';
import type {KitComponentProps} from '../../core/registry';
import {glitchAt, GlitchWrap} from './fx';
import {arr, atTime, clamp01, jitter, num, obj, P, random, str, useUid} from './util';

type Mouth = 'flat' | 'smile' | 'frown' | 'wavy' | 'tight' | 'o' | 'scream' | 'grin' | 'smirk';
type Face = {
	eye: number; // openness (1 normal)
	pupil: number; // pupil scale (1 normal, 0.35 pinpoint)
	lid: number; // upper-lid droop 0..1
	lidTilt: number; // + inner corner down (angry), - inner up (sad)
	brow: number; // + angry, - worried
	browY: number; // - raises brows
	mouth: Mouth;
	mouthW?: number;
	sweat?: boolean;
	shadow?: number; // under-eye bruise shading
	pale?: number; // cold blue cast
	blush?: number;
	lines?: boolean; // shock lines over the head
	shake?: boolean; // trembling pupils
	stare?: boolean; // fixed, unblinking, pupils locked dead centre (ignores lookX/lookY)
	talkAmp?: number; // how far the mouth opens while talking (1; a stare talks through barely-parted lips)
};

/** Expression library. Protagonist set: the first 8; neighbour set: neutral, smile, grin, blank, angry, sad, surprised, sly. */
export const EXPRESSIONS: Record<string, Face> = {
	neutral: {eye: 1, pupil: 1, lid: 0.12, lidTilt: 0, brow: 0, browY: 0, mouth: 'flat'},
	worried: {eye: 1.05, pupil: 0.85, lid: 0.05, lidTilt: -6, brow: -18, browY: -8, mouth: 'wavy', sweat: true, shadow: 0.35},
	scared: {eye: 1.25, pupil: 0.55, lid: 0, lidTilt: 0, brow: -24, browY: -14, mouth: 'frown', sweat: true, shadow: 0.55, pale: 0.35, shake: true},
	terrified: {eye: 1.42, pupil: 0.34, lid: 0, lidTilt: 0, brow: -28, browY: -20, mouth: 'scream', sweat: true, shadow: 0.85, pale: 0.6, lines: true, shake: true},
	suspicious: {eye: 0.8, pupil: 0.9, lid: 0.5, lidTilt: 8, brow: 14, browY: 4, mouth: 'tight'},
	shocked: {eye: 1.35, pupil: 0.5, lid: 0, lidTilt: 0, brow: -6, browY: -24, mouth: 'o', lines: true, pale: 0.2},
	relieved: {eye: 0.9, pupil: 1, lid: 0.4, lidTilt: -4, brow: -10, browY: -2, mouth: 'smile', blush: 0.4},
	angry: {eye: 0.95, pupil: 0.8, lid: 0.32, lidTilt: 16, brow: 24, browY: 8, mouth: 'tight', blush: 0.25},
	smile: {eye: 0.92, pupil: 0.9, lid: 0.28, lidTilt: -2, brow: -4, browY: -2, mouth: 'smile'},
	grin: {eye: 1.25, pupil: 0.26, lid: 0, lidTilt: -3, brow: 16, browY: -2, mouth: 'grin', mouthW: 86, shadow: 0.95, pale: 0.3, stare: true},
	// unblinking fixed stare that talks with barely moving lips (the "It's Management" voice at the door)
	stare: {eye: 1.14, pupil: 0.3, lid: 0, lidTilt: 0, brow: 6, browY: -6, mouth: 'flat', mouthW: 50, shadow: 0.8, pale: 0.35, stare: true, talkAmp: 0.3},
	blank: {eye: 1.08, pupil: 0.3, lid: 0.05, lidTilt: 0, brow: 0, browY: 0, mouth: 'flat', shadow: 0.75, pale: 0.35},
	sad: {eye: 0.92, pupil: 0.9, lid: 0.32, lidTilt: -12, brow: -20, browY: -4, mouth: 'frown'},
	surprised: {eye: 1.3, pupil: 0.8, lid: 0, lidTilt: 0, brow: -4, browY: -20, mouth: 'o'},
	sly: {eye: 0.75, pupil: 0.9, lid: 0.52, lidTilt: 6, brow: 10, browY: 0, mouth: 'smirk', shadow: 0.3},
};

type Spec = {
	key: string;
	skin: string;
	skinShade: string;
	headRx: number;
	headRy: number;
	headCy: number;
	eyeY: number;
	eyeDX: number;
	eyeRx: number;
	mouthY: number;
	line: string;
};

const NORA: Spec = {key: 'nora', skin: '#e8d9c4', skinShade: '#cdb99f', headRx: 142, headRy: 150, headCy: 250, eyeY: 268, eyeDX: 56, eyeRx: 30, mouthY: 352, line: P.line};
const HALE: Spec = {key: 'hale', skin: '#cfc6b6', skinShade: '#ada392', headRx: 122, headRy: 168, headCy: 246, eyeY: 256, eyeDX: 50, eyeRx: 26, mouthY: 362, line: P.line};

// ---------------------------------------------------------------- face parts

const Eye: React.FC<{
	cx: number;
	cy: number;
	rx: number;
	f: Face;
	open: number;
	look: [number, number];
	side: 1 | -1;
	skin: string;
	line: string;
	uid: string;
	t: number;
}> = ({cx, cy, rx, f, open, look, side, skin, line, uid, t}) => {
	const ry = rx * 1.12 * f.eye * open;
	if (open < 0.18) {
		return <path d={`M ${cx - rx} ${cy} Q ${cx} ${cy + rx * 0.45} ${cx + rx} ${cy}`} stroke={line} strokeWidth={6} fill="none" strokeLinecap="round" />;
	}
	const pr = rx * 0.48 * f.pupil;
	const jx = f.shake ? jitter(`${uid}px`, t, 1 / 24) * 2.2 : 0;
	const jy = f.shake ? jitter(`${uid}py`, t, 1 / 24) * 2.2 : 0;
	const px = cx + look[0] * rx * 0.45 + jx;
	const py = cy + look[1] * ry * 0.35 + jy;
	const lidH = f.lid * ry * 2;
	const tilt = f.lidTilt * side; // side = +1 for the left eye (inner corner on the right)
	const clip = `${uid}-clip`;
	return (
		<g>
			<defs>
				<clipPath id={clip}>
					<ellipse cx={cx} cy={cy} rx={rx} ry={ry} />
				</clipPath>
			</defs>
			<ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="#f6f2ea" />
			<g clipPath={`url(#${clip})`}>
				<circle cx={px} cy={py} r={pr} fill="#16151b" />
				<circle cx={px - pr * 0.35} cy={py - pr * 0.4} r={Math.max(2, pr * 0.28)} fill="#fff" />
				{lidH > 0.5 ? (
					<g transform={`rotate(${tilt} ${cx} ${cy})`}>
						<rect x={cx - rx * 1.6} y={cy - ry - 60} width={rx * 3.2} height={60 + lidH} fill={skin} />
						<line x1={cx - rx * 1.6} x2={cx + rx * 1.6} y1={cy - ry + lidH} y2={cy - ry + lidH} stroke={line} strokeWidth={7} />
					</g>
				) : null}
			</g>
			<ellipse cx={cx} cy={cy} rx={rx} ry={ry} fill="none" stroke={line} strokeWidth={5} />
		</g>
	);
};

function mouthPath(m: Mouth, cx: number, cy: number, w: number): React.ReactNode {
	const s = w / 60;
	const L = P.line;
	const st = {stroke: L, strokeWidth: 6, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
	switch (m) {
		case 'flat':
			return <path d={`M ${cx - 26 * s} ${cy} L ${cx + 26 * s} ${cy}`} {...st} />;
		case 'smile':
			return <path d={`M ${cx - 32 * s} ${cy - 6} Q ${cx} ${cy + 22 * s} ${cx + 32 * s} ${cy - 6}`} {...st} />;
		case 'frown':
			return <path d={`M ${cx - 28 * s} ${cy + 10} Q ${cx} ${cy - 12 * s} ${cx + 28 * s} ${cy + 10}`} {...st} />;
		case 'wavy':
			return <path d={`M ${cx - 30 * s} ${cy + 3} Q ${cx - 15 * s} ${cy - 8} ${cx} ${cy + 3} T ${cx + 30 * s} ${cy + 3}`} {...st} />;
		case 'tight':
			return (
				<g>
					<rect x={cx - 26 * s} y={cy - 7} width={52 * s} height={14} rx={6} fill="#f2ede4" stroke={L} strokeWidth={5} />
					<line x1={cx - 26 * s} x2={cx + 26 * s} y1={cy} y2={cy} stroke={L} strokeWidth={3} />
				</g>
			);
		case 'o':
			return (
				<g>
					<ellipse cx={cx} cy={cy + 4} rx={17 * s} ry={24 * s} fill="#2a1a20" stroke={L} strokeWidth={5} />
					<ellipse cx={cx} cy={cy + 18 * s} rx={10 * s} ry={6 * s} fill="#a5525b" />
				</g>
			);
		case 'scream':
			// terror: a tall, narrow dark oval (a frozen gasp), slightly pinched at the top, no teeth (a teeth row
			// curving under the top lip read as a laugh), a trembling wavy line under it. Stays inside the chin.
			return (
				<g>
					<path
						d={`M ${cx} ${cy - 6 * s} C ${cx + 11 * s} ${cy - 6 * s} ${cx + 15 * s} ${cy + 8 * s} ${cx + 14 * s} ${cy + 18 * s} C ${cx + 13 * s} ${cy + 30 * s} ${cx + 7 * s} ${cy + 36 * s} ${cx} ${cy + 36 * s} C ${cx - 7 * s} ${cy + 36 * s} ${cx - 13 * s} ${cy + 30 * s} ${cx - 14 * s} ${cy + 18 * s} C ${cx - 15 * s} ${cy + 8 * s} ${cx - 11 * s} ${cy - 6 * s} ${cx} ${cy - 6 * s} Z`}
						fill="#1c1016"
						stroke={L}
						strokeWidth={5}
						strokeLinejoin="round"
					/>
					<ellipse cx={cx} cy={cy + 28 * s} rx={7 * s} ry={4 * s} fill="#4a2129" />
					<path d={`M ${cx - 15 * s} ${cy + 43 * s} q ${5 * s} ${-3.5 * s} ${10 * s} 0 t ${10 * s} 0 t ${10 * s} 0`} stroke={L} strokeWidth={3} fill="none" strokeLinecap="round" opacity={0.8} />
				</g>
			);
		case 'grin': {
			// too wide, corners hiked up past the cheeks, a dark gum line and too many teeth
			const gw = 74 * s;
			const up = 26 * s;
			const teeth = Array.from({length: 13}, (_, i) => -gw + ((i + 1) * 2 * gw) / 14);
			return (
				<g>
					<path d={`M ${cx - gw} ${cy - up} Q ${cx} ${cy + 62 * s} ${cx + gw} ${cy - up} Q ${cx} ${cy + 6 * s} ${cx - gw} ${cy - up} Z`} fill="#3a1218" stroke={L} strokeWidth={5} strokeLinejoin="round" />
					<path d={`M ${cx - gw * 0.92} ${cy - up * 0.82} Q ${cx} ${cy + 52 * s} ${cx + gw * 0.92} ${cy - up * 0.82} Q ${cx} ${cy + 12 * s} ${cx - gw * 0.92} ${cy - up * 0.82} Z`} fill="#efe8d8" />
					{teeth.map((dx, i) => (
						<line key={i} x1={cx + dx} x2={cx + dx * 0.94} y1={cy + 10 * s - (Math.abs(dx) / gw) * up * 0.9} y2={cy + 40 * s - (Math.abs(dx) / gw) * up * 1.6} stroke={L} strokeWidth={2.5} />
					))}
					<path d={`M ${cx - gw * 0.9} ${cy - up * 0.6} Q ${cx} ${cy + 30 * s} ${cx + gw * 0.9} ${cy - up * 0.6}`} stroke={L} strokeWidth={2.5} fill="none" />
				</g>
			);
		}
		case 'smirk':
			return <path d={`M ${cx - 28 * s} ${cy + 4} Q ${cx + 4 * s} ${cy + 10} ${cx + 32 * s} ${cy - 12}`} {...st} />;
	}
}

const TalkMouth: React.FC<{cx: number; cy: number; open: number; w: number}> = ({cx, cy, open, w}) => (
	<g>
		<ellipse cx={cx} cy={cy + 4} rx={(18 + 6 * open) * (w / 60)} ry={4 + 20 * open} fill="#2a1a20" stroke={P.line} strokeWidth={5} />
		{open > 0.3 ? <ellipse cx={cx} cy={cy + 4 + 12 * open} rx={10 * (w / 60)} ry={5 * open} fill="#a5525b" /> : null}
	</g>
);

// ---------------------------------------------------------------- bodies / hair

const NoraBehind: React.FC<{c: Record<string, string>}> = ({c}) => (
	<g>
		{/* back of the bob */}
		<path d="M 92 250 Q 86 86 250 78 Q 414 86 408 250 L 414 352 Q 388 370 362 346 L 138 346 Q 112 370 86 352 Z" fill={c.hair} stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
	</g>
);

const NoraFront: React.FC<{c: Record<string, string>}> = ({c}) => (
	<g>
		<path
			d="M 104 236 Q 106 96 250 90 Q 394 96 396 236 L 380 214 L 368 176 L 340 196 L 318 160 L 290 186 L 262 158 L 236 186 L 206 160 L 184 192 L 156 168 L 140 210 L 120 200 Z"
			fill={c.hair}
			stroke={P.line}
			strokeWidth={6}
			strokeLinejoin="round"
		/>
		<path d="M 160 120 Q 220 98 290 104" stroke="#3b3a46" strokeWidth={8} fill="none" strokeLinecap="round" />
		{/* side locks over the cheeks */}
		<path d="M 104 230 Q 100 300 120 350 Q 130 300 132 240 Z" fill={c.hair} stroke={P.line} strokeWidth={5} strokeLinejoin="round" />
		<path d="M 396 230 Q 400 300 380 350 Q 370 300 368 240 Z" fill={c.hair} stroke={P.line} strokeWidth={5} strokeLinejoin="round" />
	</g>
);

const NoraBody: React.FC<{c: Record<string, string>}> = ({c}) => (
	<g>
		{/* neck: joins the chin to the hood (no gap under the head) */}
		<path d="M 212 352 L 208 478 L 292 478 L 288 352 Z" fill={c.skinShade} stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
		{/* hood bunched behind the neck, rising to meet the jaw */}
		<path d="M 146 446 Q 250 380 354 446 Q 362 500 250 506 Q 138 500 146 446 Z" fill={c.topShade} stroke={P.line} strokeWidth={6} />
		<path d="M 70 780 Q 66 560 150 488 Q 200 468 250 476 Q 300 468 350 488 Q 434 560 430 780 Z" fill={c.top} stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
		<path d="M 196 482 Q 250 520 304 482" stroke={P.line} strokeWidth={5} fill="none" />
		<path d="M 226 500 L 222 590 M 274 500 L 278 590" stroke="#d8d2c2" strokeWidth={5} strokeLinecap="round" />
		<circle cx={222} cy={594} r={6} fill="#d8d2c2" />
		<circle cx={278} cy={594} r={6} fill="#d8d2c2" />
		<path d="M 150 700 L 350 700 L 330 780 L 170 780 Z" fill={c.topShade} opacity={0.55} />
		<path d="M 128 560 Q 120 660 128 780 M 372 560 Q 380 660 372 780" stroke={c.topShade} strokeWidth={6} fill="none" />
	</g>
);

const HaleBehind: React.FC<{c: Record<string, string>}> = () => null;

const HaleFront: React.FC<{c: Record<string, string>}> = ({c}) => (
	<g>
		<path d="M 130 196 Q 132 84 250 78 Q 368 84 370 196 Q 344 128 252 124 Q 178 126 130 196 Z" fill={c.hair} stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
		<path d="M 160 150 Q 230 104 344 140 M 172 132 Q 240 96 330 116" stroke="#5c5c66" strokeWidth={4} fill="none" strokeLinecap="round" />
		{/* temples greying */}
		<path d="M 130 196 Q 128 228 134 250" stroke={c.hair} strokeWidth={10} strokeLinecap="round" />
		<path d="M 370 196 Q 372 228 366 250" stroke={c.hair} strokeWidth={10} strokeLinecap="round" />
	</g>
);

const HaleBody: React.FC<{c: Record<string, string>}> = ({c}) => (
	<g>
		<path d="M 222 380 L 220 470 L 280 470 L 278 380 Z" fill={c.skinShade} stroke={P.line} strokeWidth={6} />
		<path d="M 84 780 Q 84 560 160 500 Q 200 474 250 470 Q 300 474 340 500 Q 416 560 416 780 Z" fill={c.top} stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
		{/* shirt in the V of the cardigan */}
		<path d="M 206 476 L 250 610 L 294 476 Q 250 490 206 476 Z" fill={c.shirt} stroke={P.line} strokeWidth={5} />
		<path d="M 226 478 L 250 500 L 274 478" stroke="#e7e2d6" strokeWidth={6} fill="none" strokeLinejoin="round" />
		<path d="M 250 610 L 250 780" stroke={P.line} strokeWidth={5} />
		{[650, 712].map((y) => (
			<circle key={y} cx={262} cy={y} r={8} fill="#c9b48a" stroke={P.line} strokeWidth={3} />
		))}
		<path d="M 130 600 Q 124 690 132 780 M 370 600 Q 376 690 368 780" stroke={c.topShade} strokeWidth={6} fill="none" />
		<path d="M 300 650 L 350 650 L 350 700 L 300 700 Z" fill={c.topShade} stroke={P.line} strokeWidth={4} />
	</g>
);

// ---------------------------------------------------------------- arms / poses

const Arms: React.FC<{pose: string; c: Record<string, string>; skin: string; t: number; glow: string}> = ({pose, c, skin, t, glow}) => {
	const sleeve = (d: string, k: string) => (
		<g key={k}>
			<path d={d} stroke={P.line} strokeWidth={82} fill="none" strokeLinecap="round" />
			<path d={d} stroke={c.top} strokeWidth={70} fill="none" strokeLinecap="round" />
		</g>
	);
	const hand = (x: number, y: number, r: number, k: string) => <ellipse key={k} cx={x} cy={y} rx={r} ry={r * 0.86} fill={skin} stroke={P.line} strokeWidth={5} />;
	if (pose === 'phone') {
		const b = Math.sin(t * 1.6) * 3;
		return (
			<g>
				{sleeve(`M 120 760 Q 150 640 210 ${600 + b}`, 'l')}
				{sleeve(`M 380 760 Q 350 640 290 ${600 + b}`, 'r')}
				<g transform={`translate(0 ${b}) rotate(-6 250 560)`}>
					<rect x={192} y={470} width={116} height={200} rx={18} fill="#121317" stroke={P.line} strokeWidth={5} />
					<rect x={200} y={478} width={100} height={184} rx={12} fill={glow} />
					<rect x={208} y={500} width={56} height={14} rx={7} fill="rgba(255,255,255,0.65)" />
					<rect x={232} y={526} width={60} height={14} rx={7} fill="rgba(255,255,255,0.45)" />
					<rect x={208} y={552} width={70} height={14} rx={7} fill="rgba(255,255,255,0.65)" />
				</g>
				{hand(206, 606 + b, 34, 'hl')}
				{hand(294, 606 + b, 34, 'hr')}
			</g>
		);
	}
	if (pose === 'sit') {
		// sitting on the floor with her back to the door: knees drawn up to the chest, arms locked round them
		const b = Math.sin(t * 1.3) * 2;
		return (
			<g transform={`translate(0 ${b})`}>
				<path d="M 96 790 Q 92 600 170 560 Q 236 532 262 600 Q 280 690 270 790 Z" fill="#2c3038" stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
				<path d="M 404 790 Q 408 600 330 560 Q 264 532 238 600 Q 220 690 230 790 Z" fill="#33373f" stroke={P.line} strokeWidth={6} strokeLinejoin="round" />
				{sleeve('M 96 600 Q 150 690 250 676', 'l')}
				{sleeve('M 404 600 Q 350 690 250 676', 'r')}
				{hand(226, 676, 30, 'hl')}
				{hand(274, 672, 30, 'hr')}
			</g>
		);
	}
	if (pose === 'ear') {
		return (
			<g>
				{sleeve('M 400 780 Q 452 560 404 410', 'r')}
				<rect x={370} y={250} width={64} height={120} rx={12} fill="#121317" stroke={P.line} strokeWidth={5} transform="rotate(14 402 310)" />
				{hand(404, 372, 40, 'hr')}
			</g>
		);
	}
	if (pose === 'cover') {
		return (
			<g>
				{sleeve('M 110 780 Q 150 560 214 392', 'l')}
				{sleeve('M 390 780 Q 350 560 286 392', 'r')}
				{hand(222, 362, 44, 'hl')}
				{hand(278, 368, 44, 'hr')}
			</g>
		);
	}
	return null;
};

// ---------------------------------------------------------------- puppet

type Talk = {at?: number; until?: number} | [number, number];

function talkOpen(talk: unknown, t: number, seed: string): number {
	for (const r of arr<Talk>(talk)) {
		const a = Array.isArray(r) ? r[0] : num(r.at, 0);
		const b = Array.isArray(r) ? r[1] : num(r.until, a + 1);
		if (t >= a && t < b) {
			const step = Math.floor(t * 11);
			const v = random(`${seed}-talk-${step}`);
			return v < 0.25 ? 0.1 : v < 0.6 ? 0.55 : 1;
		}
	}
	return -1;
}

function blinkOpen(t: number, seed: string): number {
	// blinks every 2.4-4.4 s, closed ~0.11 s
	let tt = random(`${seed}-b0`) * 2;
	let i = 0;
	while (tt < t + 1 && i < 200) {
		const d = t - tt;
		if (d >= 0 && d < 0.13) return d < 0.04 || d > 0.09 ? 0.45 : 0.05;
		tt += 2.4 + random(`${seed}-b${++i}`) * 2;
	}
	return 1;
}

const Puppet: React.FC<KitComponentProps & {spec: Spec; colors: Record<string, string>}> = ({props, time: t, width, height, spec, colors}) => {
	const uid = useUid(spec.key);
	const exprs = arr<{t?: number; e?: string}>(props.exprs);
	const ex = exprs.length ? atTime(exprs, t) : {item: {e: str(props.expr, 'neutral')}, since: 99};
	const name = str(ex.item?.e, 'neutral');
	const f = EXPRESSIONS[name] ?? EXPRESSIONS.neutral;
	const swapPop = ex.since < 0.14 ? 1 + 0.035 * (1 - ex.since / 0.14) : 1;
	const pose = str(props.pose, 'idle');
	const glow = str(props.glow, '#a9c6ff');
	const look: [number, number] = f.stare ? [0, 0] : [num(props.lookX, 0), num(props.lookY, 0)];
	const open = props.blink === false || f.stare ? 1 : blinkOpen(t + num(props.blinkOffset, 0), `${spec.key}-${str(props.seed, '')}`);
	const tk = talkOpen(props.talk, t, spec.key);
	const breathe = 1 + Math.sin(t * 2.1) * 0.008;
	const tilt = num(props.tilt, 0) + Math.sin(t * 0.9) * 0.8;
	const c = {...colors, ...(Object.fromEntries(Object.entries(obj(props.colors)).filter(([, v]) => typeof v === 'string')) as Record<string, string>)};
	const skin = c.skin ?? spec.skin;
	const {headRx, headRy, headCy, eyeY, eyeDX, eyeRx, mouthY} = spec;
	const isNora = spec.key === 'nora';
	const light = str(props.light, pose === 'phone' ? 'phone' : 'none');
	const silhouette = Boolean(props.silhouette);
	const sweatY = ((t * 18) % 60) - 10;

	const head = (
		<g transform={`rotate(${tilt} 250 ${headCy + headRy}) translate(250 ${headCy}) scale(${swapPop}) translate(-250 ${-headCy})`}>
			{isNora ? <NoraBehind c={c} /> : <HaleBehind c={c} />}
			{!isNora ? (
				<>
					<ellipse cx={250 - headRx + 4} cy={eyeY + 20} rx={22} ry={34} fill={skin} stroke={P.line} strokeWidth={5} />
					<ellipse cx={250 + headRx - 4} cy={eyeY + 20} rx={22} ry={34} fill={skin} stroke={P.line} strokeWidth={5} />
				</>
			) : null}
			<ellipse cx={250} cy={headCy} rx={headRx} ry={headRy} fill={skin} stroke={P.line} strokeWidth={6} />
			{/* cheek / jaw shade */}
			<path d={`M ${250 - headRx * 0.8} ${headCy + headRy * 0.45} Q 250 ${headCy + headRy * 1.08} ${250 + headRx * 0.8} ${headCy + headRy * 0.45} Q 250 ${headCy + headRy * 0.9} ${250 - headRx * 0.8} ${headCy + headRy * 0.45} Z`} fill={spec.skinShade} opacity={0.5} />
			{!isNora ? (
				<>
					{/* sunken sockets */}
					<ellipse cx={250 - eyeDX} cy={eyeY + 4} rx={eyeRx * 1.55} ry={eyeRx * 1.6} fill="#8d8273" opacity={0.45} />
					<ellipse cx={250 + eyeDX} cy={eyeY + 4} rx={eyeRx * 1.55} ry={eyeRx * 1.6} fill="#8d8273" opacity={0.45} />
					<path d={`M 250 ${eyeY + 20} L 238 ${eyeY + 68} Q 250 ${eyeY + 76} 262 ${eyeY + 68}`} stroke={P.line} strokeWidth={4} fill="none" strokeLinejoin="round" />
				</>
			) : (
				<path d={`M 250 ${eyeY + 34} q -6 14 4 16`} stroke={P.line} strokeWidth={4} fill="none" strokeLinecap="round" />
			)}
			{(f.shadow ?? 0) > 0 ? (
				<g opacity={(f.shadow ?? 0) * 0.75}>
					<ellipse cx={250 - eyeDX} cy={eyeY + eyeRx * 1.35} rx={eyeRx * 1.25} ry={eyeRx * 0.5} fill="#6f5c86" />
					<ellipse cx={250 + eyeDX} cy={eyeY + eyeRx * 1.35} rx={eyeRx * 1.25} ry={eyeRx * 0.5} fill="#6f5c86" />
				</g>
			) : null}
			{(f.blush ?? 0) > 0 ? (
				<g opacity={f.blush}>
					<ellipse cx={250 - eyeDX - 22} cy={eyeY + 56} rx={26} ry={12} fill="#d98c8c" />
					<ellipse cx={250 + eyeDX + 22} cy={eyeY + 56} rx={26} ry={12} fill="#d98c8c" />
				</g>
			) : null}
			{(f.pale ?? 0) > 0 ? <ellipse cx={250} cy={headCy} rx={headRx - 3} ry={headRy - 3} fill="#7f9cc4" opacity={(f.pale ?? 0) * 0.32} /> : null}
			<Eye cx={250 - eyeDX} cy={eyeY} rx={eyeRx} f={f} open={open} look={look} side={1} skin={skin} line={P.line} uid={`${uid}l`} t={t} />
			<Eye cx={250 + eyeDX} cy={eyeY} rx={eyeRx} f={f} open={open} look={look} side={-1} skin={skin} line={P.line} uid={`${uid}r`} t={t} />
			{/* brows */}
			{[-1, 1].map((sd) => {
				const bx = 250 + sd * eyeDX;
				const by = eyeY - eyeRx * 1.12 * Math.max(1, f.eye) - 22 + f.browY;
				const ang = -sd * f.brow;
				return (
					<path
						key={sd}
						d={`M ${bx - 34} ${by} Q ${bx} ${by - 8} ${bx + 34} ${by}`}
						transform={`rotate(${ang} ${bx} ${by})`}
						stroke={isNora ? c.hair : '#4a4a52'}
						strokeWidth={isNora ? 12 : 10}
						fill="none"
						strokeLinecap="round"
					/>
				);
			})}
			{!isNora ? (
				<path d={`M ${250 - 40} ${mouthY - 22} Q 250 ${mouthY - 34} ${250 + 40} ${mouthY - 22}`} stroke="#3e3d45" strokeWidth={9} fill="none" strokeLinecap="round" />
			) : null}
			{tk >= 0 && f.mouth !== 'scream' && f.mouth !== 'grin' ? <TalkMouth cx={250} cy={mouthY} open={tk * (f.talkAmp ?? 1)} w={f.talkAmp !== undefined ? 46 : 60} /> : mouthPath(f.mouth, 250, mouthY, f.mouthW ?? 60)}
			{isNora ? <NoraFront c={c} /> : <HaleFront c={c} />}
			{f.sweat ? (
				<path
					d={`M ${250 + headRx - 30} ${headCy - 60 + sweatY} q -14 22 0 30 q 14 -8 0 -30 Z`}
					fill="#bfe0f2"
					stroke={P.line}
					strokeWidth={4}
					opacity={clamp01(1 - sweatY / 55)}
				/>
			) : null}
			{f.lines ? (
				<g stroke={P.line} strokeWidth={7} strokeLinecap="round">
					<line x1={250 + headRx * 0.55} y1={headCy - headRy - 10} x2={250 + headRx * 0.75} y2={headCy - headRy - 46} />
					<line x1={250 + headRx * 0.85} y1={headCy - headRy + 14} x2={250 + headRx * 1.12} y2={headCy - headRy - 16} />
					<line x1={250 + headRx * 1.0} y1={headCy - headRy + 52} x2={250 + headRx * 1.32} y2={headCy - headRy + 34} />
				</g>
			) : null}
			{light === 'phone' ? (
				<ellipse cx={250} cy={headCy + headRy * 0.55} rx={headRx * 0.98} ry={headRy * 0.62} fill={`url(#${uid}-glow)`} style={{mixBlendMode: 'screen'}} />
			) : null}
			{light === 'red' ? (
				<ellipse cx={250} cy={headCy + headRy * 0.95} rx={headRx * 1.25} ry={headRy * 0.85} fill={`url(#${uid}-under)`} style={{mixBlendMode: 'screen'}} />
			) : null}
		</g>
	);

	const figure = (
		<svg width={width} height={height} viewBox="0 0 500 760" preserveAspectRatio="xMidYMax meet" style={{overflow: 'visible', display: 'block'}}>
			<defs>
				<radialGradient id={`${uid}-glow`} cx="50%" cy="80%" r="60%">
					<stop offset="0" stopColor={glow} stopOpacity={0.55} />
					<stop offset="1" stopColor={glow} stopOpacity={0} />
				</radialGradient>
				<radialGradient id={`${uid}-under`} cx="50%" cy="95%" r="65%">
					<stop offset="0" stopColor="#ff2a2a" stopOpacity={0.75} />
					<stop offset="1" stopColor="#ff2a2a" stopOpacity={0} />
				</radialGradient>
				<filter id={`${uid}-red`} colorInterpolationFilters="sRGB">
					<feColorMatrix type="matrix" values="0.92 0.1 0.04 0 0.03  0.05 0.66 0.05 0 0  0.05 0.05 0.66 0 0  0 0 0 1 0" />
				</filter>
				<filter id={`${uid}-sil`}>
					<feColorMatrix type="matrix" values="0 0 0 0 0.04  0 0 0 0 0.045  0 0 0 0 0.06  0 0 0 1 0" />
				</filter>
			</defs>
			<g filter={silhouette ? `url(#${uid}-sil)` : light === 'red' ? `url(#${uid}-red)` : undefined}>
				<g transform={`translate(250 780) scale(1 ${breathe}) translate(-250 -780)`}>{isNora ? <NoraBody c={c} /> : <HaleBody c={c} />}</g>
				{head}
				<Arms pose={pose} c={c} skin={skin} t={t} glow={glow} />
			</g>
			{silhouette ? (
				<g>
					<circle cx={250 - eyeDX} cy={eyeY} r={9} fill="#f2f2ea" />
					<circle cx={250 + eyeDX} cy={eyeY} r={9} fill="#f2f2ea" />
					{f.mouth === 'grin' ? mouthPath('grin', 250, mouthY, f.mouthW ?? 60) : null}
				</g>
			) : null}
		</svg>
	);

	return (
		<div style={{width, height, position: 'relative'}}>
			<GlitchWrap amount={glitchAt(props, t)} t={t} seed={spec.key}>
				{figure}
			</GlitchWrap>
		</div>
	);
};

/**
 * props (both characters):
 *   expr ('neutral') or exprs [{t, e}]   expression name(s) from EXPRESSIONS (scene seconds)
 *   talk [[from, to], ...] or [{at, until}]   mouth flap windows
 *   pose 'idle' | 'phone' (reading a glowing phone) | 'ear' (phone call) | 'cover' (hands over mouth) | 'sit' (on the floor, hugging her knees)
 *   lookX, lookY (-1..1)   pupil direction        tilt (deg)
 *   light 'none' | 'phone' | 'red'                 silhouette (bool: black shape + eye glints)
 *   blink (true), blinkOffset, seed, colors {hair, top, topShade, skin, shirt}, glow, glitch
 */
export const Protagonist: React.FC<KitComponentProps> = (p) => (
	<Puppet {...p} spec={NORA} colors={{hair: '#24232b', top: '#56603f', topShade: '#454d32', skinShade: NORA.skinShade}} />
);
export const Neighbour: React.FC<KitComponentProps> = (p) => (
	<Puppet {...p} spec={HALE} colors={{hair: '#34343b', top: '#5b2c35', topShade: '#47212a', shirt: '#2d3036', skinShade: HALE.skinShade}} />
);
