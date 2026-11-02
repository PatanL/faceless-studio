/**
 * stick/Turk: the chess automaton and its cabinet (our own drawing), front view, 900 x 1000 box, castors on the
 * bottom edge. Flat style A: wood in ochre ramps, one shadow shape per part, brass gears.
 *
 * props (numbers may be [{t, v, ease}] tracks; times are scene-local seconds, "@word" anchors resolve)
 *   doorL, doorR, doorR2, drawer   0..1 how far each front door / the drawer is open
 *   candle      0..1 a candle glow behind the open compartments (light through the gears)
 *   spin        gear speed (turns per second while > 0); tick: true makes it a ratchet tick
 *   arm         0 rest (hand on the cushion) .. 1 raised;  reach 0..1 hand across the board (with arm 1)
 *   sweepAt     time the arm sweeps the board (pieces fly off)
 *   look        -1..1 the painted eyes
 *   cut         0..1 cutaway: the front comes off and shows the inside (hidden master, fake gear panel)
 *   seat        0..1 the master's sliding seat (0 = left, behind the gear panel; 1 = right)
 *   masterFace  face of the hidden master ([{t, v}]); masterCandle true: he holds a candle
 *   magnets     [{t, i}] an iron marker under square i (0..7) jumps up and glows at t
 *   lever       0..1 shows the lever rod from his hand up to the Turk's arm
 *   pieces      true (default): pieces on the board
 *   char        0..1 burnt (darkens to indigo ash)
 *   xray        0..1 on the cutaway, the doors stay as see-through ghosts (shows which door is open)
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {arr, bool, clamp, lerp, num, track, easeOut} from '../util';
import {c, K, f, step} from './common';
import {PersonBody} from './person';
import {mixOk} from '../house/color';

type P2 = [number, number];

function Gear({x, y, r, teeth, rot, fill, shade}: {x: number; y: number; r: number; teeth: number; rot: number; fill: string; shade: string}) {
	const pts: string[] = [];
	const n = teeth * 2;
	for (let i = 0; i < n; i++) {
		const a0 = (i / n) * Math.PI * 2;
		const a1 = ((i + 1) / n) * Math.PI * 2;
		const rr = i % 2 === 0 ? r : r * 0.82;
		pts.push(`${f(Math.cos(a0) * rr)} ${f(Math.sin(a0) * rr)}`, `${f(Math.cos(a1) * rr)} ${f(Math.sin(a1) * rr)}`);
	}
	return (
		<g transform={`translate(${f(x)} ${f(y)}) rotate(${f(rot)})`}>
			<path d={`M ${pts.join(' L ')} Z`} fill={fill} />
			<circle r={r * 0.6} fill={shade} />
			<circle r={r * 0.46} fill={fill} />
			{[0, 1, 2, 3].map((k) => (
				<rect key={k} x={-r * 0.05} y={-r * 0.46} width={r * 0.1} height={r * 0.92} fill={shade}
					transform={`rotate(${k * 45})`} />
			))}
			<circle r={r * 0.14} fill={shade} />
		</g>
	);
}

/** a door hinged at hx (left edge) or at its right edge (dir -1), swinging out toward the viewer */
function Door({hx, y0, y1, w, open, dir, wood, shade}: {hx: number; y0: number; y1: number; w: number; open: number; dir: 1 | -1; wood: string; shade: string}) {
	const th = clamp(open) * (Math.PI / 2) * 0.92;
	const ex = hx + dir * w * Math.cos(th);
	const k = 26 * Math.sin(th);
	const back = open > 0.55;
	const d = `M ${f(hx)} ${f(y0)} L ${f(ex)} ${f(y0 - k)} L ${f(ex)} ${f(y1 + k)} L ${f(hx)} ${f(y1)} Z`;
	const inset = (s: number) => {
		const ix0 = hx + dir * 16 * Math.cos(th);
		const ix1 = hx + dir * (w - 16) * Math.cos(th);
		return `M ${f(ix0)} ${f(y0 + 18 - k * 0.1 * s)} L ${f(ix1)} ${f(y0 + 18 - k * 0.9)} L ${f(ix1)} ${f(y1 - 18 + k * 0.9)} L ${f(ix0)} ${f(y1 - 18)} Z`;
	};
	return (
		<g>
			<path d={d} fill={back ? shade : wood} />
			{!back && <path d={inset(1)} fill={shade} opacity={0.55} />}
			{!back && <circle cx={ex - dir * 22 * Math.cos(th)} cy={(y0 + y1) / 2} r={8} fill={K.gold} />}
		</g>
	);
}

export const Turk: React.FC<KitComponentProps> = ({props, time}) => {
	const t = time;
	const char = clamp(track(props.char, t, 0));
	const tint = (col: string) => (char > 0 ? mixOk(col, c('ink-0'), char * 0.85) : col);
	const wood = tint(c('ochre-1'));
	const woodSh = tint(c('ochre-0'));
	const woodLt = tint(c('ochre-2'));
	const dark = tint(c('ink-0'));
	const doorL = clamp(track(props.doorL, t, 0));
	const doorR = clamp(track(props.doorR, t, 0));
	const doorR2 = clamp(track(props.doorR2, t, 0));
	const drawer = clamp(track(props.drawer, t, 0));
	const candle = clamp(track(props.candle, t, 0));
	const spin = track(props.spin, t, 0);
	const tick = bool(props.tick, false);
	const armUp = clamp(track(props.arm, t, 0));
	const reach = clamp(track(props.reach, t, 0));
	const look = track(props.look, t, 0);
	const cut = clamp(track(props.cut, t, 0));
	const seat = clamp(track(props.seat, t, 0));
	const lever = clamp(track(props.lever, t, 0));
	const sweepAt = num(props.sweepAt, -1);
	const xray = clamp(track(props.xray, t, 0));
	const showPieces = props.pieces !== false;
	// gear angle: smooth spin or a ratchet tick (one step every 0.5 s, snapping with an ease)
	const turns = spin > 0 ? t * spin : 0;
	const gAng = tick ? (Math.floor(turns * 6) + easeOut((turns * 6) % 1 * 3)) * 60 : turns * 360;

	// Turk right hand
	const rest: P2 = [432, 566];
	const lifted: P2 = [470, 430];
	const sweeping = sweepAt >= 0 && t >= sweepAt;
	const sw = sweeping ? easeOut(clamp((t - sweepAt) / 0.45)) : 0;
	let hand: P2 = [lerp(rest[0], lerp(lifted[0], 640, reach), armUp), lerp(rest[1], lerp(lifted[1], 560, reach), armUp)];
	if (sweeping) hand = [lerp(430, 760, sw), 560 - Math.sin(sw * Math.PI) * 18];
	const sh: P2 = [372, 372];
	const el: P2 = [lerp(sh[0], hand[0], 0.45) + 24, lerp(sh[1], hand[1], 0.45) + 46 - armUp * 30];

	const top = 586;
	const sq = 8;
	const bx0 = 400;
	const bx1 = 640;
	const magnets = arr<{t: number; i: number}>(props.magnets);

	const pieces = Array.from({length: 8}, (_, i) => {
		const px = bx0 + 16 + i * ((bx1 - bx0 - 32) / 7);
		const white = i % 2 === 0;
		if (!sweeping) return {x: px, y: top - 6, r: 0, o: 1, white};
		const dt = Math.max(0, t - sweepAt - 0.06 - (px - 400) / 900);
		const vx = 520 + (i % 3) * 140;
		const vy = -520 - (i % 4) * 90;
		return {x: px + vx * dt, y: top - 6 + vy * dt + 1500 * dt * dt, r: dt * (300 + i * 40), o: dt > 1.1 ? 0 : 1, white};
	});

	const masterProps = {
		costume: 'master', face: props.masterFace ?? 'focus', pose: lever > 0.5 ? 'hold' : props.masterCandle ? 'holdHigh' : 'hold',
		item: props.masterCandle ? 'candle' : 'none', seated: true, seed: 7, look: 0.5, crouch: 1,
	};
	const mx = lerp(150, 470, seat);

	return (
		<svg viewBox="0 0 900 1000" width="100%" height="100%" preserveAspectRatio="xMidYMax meet" style={{overflow: 'visible'}}>
			<ellipse cx={450} cy={972} rx={400} ry={24} fill={c('ink-1')} opacity={0.25} />
			{/* the automaton, behind the cabinet top */}
			<g>
				{/* pipe (left hand) */}
				<path d="M 236 552 L 120 330" stroke={woodSh} strokeWidth={12} strokeLinecap="round" />
				<path d="M 96 300 Q 92 350 124 352 Q 150 350 150 312 Z" fill={tint(c('ochre-0'))} />
				{/* robe body */}
				<path d="M 214 360 Q 300 320 386 360 L 410 590 L 190 590 Z" fill={tint(c('coral-2'))} />
				<path d="M 300 334 Q 352 336 386 360 L 410 590 L 318 590 Z" fill={tint(c('coral-0'))} />
				<path d="M 250 380 L 350 380 L 340 410 L 260 410 Z" fill={tint(c('amber-4'))} />
				{/* left arm to the pipe */}
				<path d="M 228 382 L 196 476 L 236 548" stroke={tint(c('coral-1'))} strokeWidth={40} strokeLinecap="round" strokeLinejoin="round" fill="none" />
				<circle cx={236} cy={550} r={22} fill={woodLt} />
				{/* fur collar */}
				<ellipse cx={300} cy={346} rx={96} ry={30} fill={tint(c('ochre-3'))} />
				<ellipse cx={330} cy={352} rx={60} ry={20} fill={tint(c('ochre-2'))} />
				{/* head: painted wooden face */}
				<ellipse cx={300} cy={262} rx={74} ry={84} fill={woodSh} />
				<ellipse cx={292} cy={254} rx={68} ry={78} fill={tint(c('ochre-2'))} />
				{[272, 332].map((x, i) => (
					<g key={i}>
						<ellipse cx={x} cy={244} rx={17} ry={13} fill={tint(c('bone-2'))} />
						<circle cx={x + 4 + look * 7} cy={245} r={7} fill={tint(c('ink-1'))} />
						<rect x={x - 20} y={218} width={40} height={10} rx={5} fill={tint(c('ink-1'))} transform={`rotate(${i ? -8 : 8} ${x} 223)`} />
					</g>
				))}
				<path d="M 236 300 Q 270 280 300 292 Q 330 280 364 300 Q 342 312 300 302 Q 258 312 236 300 Z" fill={tint(c('ink-1'))} />
				<path d="M 262 312 Q 300 330 338 312 L 300 380 Z" fill={tint(c('ink-1'))} />
				{/* turban */}
				<g transform="translate(0 -26)">
				<ellipse cx={300} cy={180} rx={110} ry={74} fill={tint(c('bone-1'))} />
				<path d="M 300 108 Q 392 112 410 180 Q 380 238 300 248 Q 360 210 360 170 Q 352 128 300 108 Z" fill={tint(c('bone-0'))} />
				<path d="M 196 196 Q 300 250 404 196 L 400 218 Q 300 270 200 218 Z" fill={tint(c('coral-2'))} />
				<circle cx={300} cy={176} r={16} fill={tint(c('magenta-2'))} />
				<path d="M 300 162 Q 318 92 352 72 Q 334 120 312 166 Z" fill={tint(c('violet-2'))} />
				</g>
				{/* right arm (the moving one) */}
				<path d={`M ${sh[0]} ${sh[1]} L ${f(el[0])} ${f(el[1])} L ${f(hand[0])} ${f(hand[1])}`} stroke={tint(c('coral-1'))} strokeWidth={40}
					strokeLinecap="round" strokeLinejoin="round" fill="none" />
				<path d={`M ${f(hand[0] - 26)} ${f(hand[1] - 4)} q 26 -22 52 0 l -6 22 q -20 8 -40 0 Z`} fill={woodLt} />
				<rect x={hand[0] - 6} y={hand[1] - 2} width={46} height={10} rx={5} fill={woodLt} transform={`rotate(20 ${hand[0]} ${hand[1]})`} />
			</g>
			{/* cabinet */}
			<rect x={102} y={top} width={696} height={26} rx={6} fill={woodLt} />
			<path d={`M 140 ${top} L 760 ${top} L 724 ${top - 26} L 176 ${top - 26} Z`} fill={wood} />
			{/* board on top */}
			{Array.from({length: sq}, (_, i) => (
				<path key={i} d={`M ${f(bx0 + (i * (bx1 - bx0)) / sq)} ${top} L ${f(bx0 + ((i + 1) * (bx1 - bx0)) / sq)} ${top} L ${f(bx0 + 10 + ((i + 1) * (bx1 - bx0 - 20)) / sq)} ${top - 24} L ${f(bx0 + 10 + (i * (bx1 - bx0 - 20)) / sq)} ${top - 24} Z`}
					fill={i % 2 ? tint(c('ink-1')) : tint(c('bone-1'))} />
			))}
			{/* cushion the hand rests on */}
			<ellipse cx={440} cy={top - 4} rx={40} ry={10} fill={tint(c('magenta-1'))} />
			{showPieces &&
				pieces.map((p, i) =>
					p.o > 0 ? (
						<g key={i} transform={`translate(${f(p.x)} ${f(p.y)}) rotate(${f(p.r)})`}>
							<path d="M -11 0 L 11 0 L 7 -18 Q 0 -24 -7 -18 Z" fill={p.white ? c('bone-2') : c('ink-0')} />
							<circle cy={-26} r={8} fill={p.white ? c('bone-2') : c('ink-0')} />
						</g>
					) : null,
				)}
			{/* front */}
			<rect x={120} y={top + 26} width={660} height={292} fill={wood} />
			<rect x={600} y={top + 26} width={180} height={292} fill={woodSh} opacity={0.6} />
			{/* compartments (visible when the doors open or the front is cut away) */}
			<g>
				<rect x={140} y={622} width={240} height={200} fill={dark} />
				<rect x={400} y={622} width={360} height={200} fill={tint(c('ink-1'))} />
				{candle > 0 && (
					<g opacity={candle}>
						<circle cx={260} cy={720} r={110} fill={c('amber-3')} opacity={0.28} />
						<circle cx={260} cy={720} r={60} fill={c('amber-4')} opacity={0.4} />
						<circle cx={580} cy={720} r={120} fill={c('amber-3')} opacity={0.22} />
					</g>
				)}
				{/* gears (left: the "machine"; on the cutaway they sit on a hinged false panel) */}
				<g opacity={1 - cut * 0.15}>
					<Gear x={200} y={690} r={52} teeth={10} rot={gAng} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
					<Gear x={290} y={760} r={44} teeth={9} rot={-gAng * 1.18 + 12} fill={tint(c('amber-4'))} shade={tint(c('amber-2'))} />
					<Gear x={330} y={668} r={30} teeth={7} rot={gAng * 1.7} fill={tint(c('ochre-2'))} shade={tint(c('ochre-0'))} />
					<Gear x={180} y={790} r={24} teeth={6} rot={-gAng * 2.1} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
				</g>
				{/* right side: a few rods and a cylinder (mostly empty) */}
				<g opacity={1 - cut}>
					<rect x={470} y={650} width={10} height={150} fill={tint(c('amber-2'))} />
					<rect x={640} y={650} width={10} height={150} fill={tint(c('amber-2'))} />
					<rect x={500} y={700} width={120} height={50} rx={25} fill={tint(c('amber-3'))} />
					<rect x={560} y={700} width={60} height={50} rx={22} fill={tint(c('amber-1'))} />
				</g>
				{/* cutaway: the hidden master on his sliding seat */}
				{cut > 0 && (
					<g opacity={clamp(cut * 1.6)}>
						<rect x={140} y={806} width={620} height={10} fill={c('amber-2')} />
						<rect x={mx + 50} y={792} width={170} height={20} rx={8} fill={c('coral-1')} />
						{/* false panel line in front of the gears */}
						<path d="M 384 624 V 820" stroke={c('bone-2')} strokeWidth={4} strokeDasharray="12 10" opacity={0.8} />
						{/* magnets: iron markers under each square on threads */}
						{Array.from({length: 8}, (_, i) => {
							const x = bx0 + 16 + i * ((bx1 - bx0 - 32) / 7);
							const hit = magnets.filter((m) => typeof m.t === 'number' && m.i === i && t >= m.t).pop();
							const age = hit ? t - hit.t : 9;
							const up = hit ? (age < 0.18 ? easeOut(age / 0.18) : 1 - clamp((age - 1.2) / 0.4)) : 0;
							const y = 680 - up * 50;
							return (
								<g key={i}>
									<path d={`M ${f(x)} 622 V ${f(y)}`} stroke={c('bone-0')} strokeWidth={2} />
									{up > 0.05 && <circle cx={x} cy={y} r={20} fill={c('coral-3')} opacity={0.45 * up} />}
									<circle cx={x} cy={y} r={11} fill={up > 0.05 ? c('coral-2') : c('dusk-3')} />
								</g>
							);
						})}
						{/* lever rod to the Turk's arm */}
						{lever > 0 && (
							<g opacity={lever}>
								<path d={`M ${f(mx + 170)} 742 L ${f(mx + 220)} 650 L 372 ${top + 10} L ${f(sh[0])} ${f(sh[1] + 40)}`} stroke={c('amber-3')}
									strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" fill="none" />
								<circle cx={mx + 220} cy={640} r={9} fill={c('amber-1')} />
							</g>
						)}
						<g transform={`translate(${f(mx - 20)} 553) scale(0.42)`}>
							<PersonBody props={masterProps} t={t} />
						</g>
					</g>
				)}
			</g>
			{/* doors and drawer (gone on the cutaway) */}
			<g opacity={cut > 0 ? Math.max(1 - clamp(cut * 2), xray * 0.4) : 1}>
				<Door hx={140} y0={622} y1={822} w={240} open={doorL} dir={1} wood={wood} shade={woodSh} />
				<Door hx={400} y0={622} y1={822} w={180} open={doorR} dir={1} wood={wood} shade={woodSh} />
				<Door hx={760} y0={622} y1={822} w={180} open={doorR2} dir={-1} wood={wood} shade={woodSh} />
				<rect x={140} y={838 + drawer * 40} width={620} height={52} rx={4} fill={woodSh} />
				<rect x={146} y={844 + drawer * 40} width={608} height={40} rx={4} fill={wood} />
				<circle cx={450} cy={864 + drawer * 40} r={8} fill={K.gold} />
			</g>
			{/* plinth + castors */}
			<rect x={110} y={900} width={680} height={22} rx={6} fill={woodSh} />
			{[160, 360, 540, 740].map((x) => (
				<g key={x}>
					<rect x={x - 8} y={918} width={16} height={22} fill={woodSh} />
					<circle cx={x} cy={950} r={20} fill={tint(c('ink-1'))} />
					<circle cx={x} cy={950} r={7} fill={K.gold} />
				</g>
			))}
		</svg>
	);
};
