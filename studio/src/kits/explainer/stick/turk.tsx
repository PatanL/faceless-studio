/**
 * stick/Turk: the chess automaton and its cabinet (our own drawing), front view, 900 x 1000 box, castors on the
 * bottom edge. Flat style A: wood in ochre ramps, one shadow shape per part, brass gears. The figure reads as a
 * machine: carved wooden face with a hinged jaw seam, brass ball joints, a stiff stepped arm.
 *
 * props (numbers may be [{t, v, ease}] tracks; times are scene-local seconds, "@word" anchors resolve under "t")
 *   doorL, doorR, doorR2, drawer   0..1 how far each front door / the drawer is open
 *   candle      0..1 a candle glow behind the open compartments (light through the gears)
 *   spin        gear speed (turns per second while > 0); tick: true makes it a ratchet tick
 *   arm         0 rest (hand on the cushion) .. 1 raised;  reach 0..1 hand across the board (with arm 1)
 *   sweep       [{t, v: 1}] the arm sweeps the board at t (pieces fly off)
 *   look        -1..1 the painted eyes
 *   cut         0..1 cutaway: the front comes off and shows the inside (hidden master, false gear panel)
 *   xray        0..1 on the cutaway, door outlines stay as dashed ghosts (which door is open)
 *   seat        0..1 the master's sliding seat (0 = left, behind the false gear panel; 1 = right)
 *   masterFace  face of the hidden master ([{t, v}]); masterCandle true: he holds a candle
 *   magnets     [{t, i}] an iron marker under square i (0..7) jumps up and glows at t
 *   lever       0..1 shows the lever rod from his hand up to the Turk's arm
 *   pieces      true (default): pieces on the board
 *   char        0..1 burnt (darkens to indigo ash);  fire 0..1 flames over it
 *   dark        0..1 the inside is dark except the candle's pool of light
 *   smoke       0..1 the candle's smoke: a dotted trail from the hidden candle up the Turk's back to the neck (on the
 *               cutaway; it never crosses the face) and puffs curling out of the top of the turban
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {arr, clamp, lerp, track, easeOut, easeInOut} from '../util';
import {c, K, f, inkG} from './common';
import {PersonBody} from './person';
import {mixOk} from '../house/color';

type P2 = [number, number];

/** time of the first keyframe whose v is truthy ([{t, v}]), or a plain number; -1 if none */
export function when(v: unknown): number {
	if (typeof v === 'number') return v;
	const k = arr<{t: number; v: unknown}>(v).filter((x) => typeof x.t === 'number' && x.v).sort((a, b) => a.t - b.t);
	return k.length ? k[0].t : -1;
}

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
				<rect key={k} x={-r * 0.05} y={-r * 0.46} width={r * 0.1} height={r * 0.92} fill={shade} transform={`rotate(${k * 45})`} />
			))}
			<circle r={r * 0.14} fill={shade} />
		</g>
	);
}

export function Flame({x, y, s, t, k}: {x: number; y: number; s: number; t: number; k: number}) {
	if (s <= 0) return null;
	const w = 1 + 0.18 * Math.sin(t * 11 + k * 1.7) + 0.08 * Math.sin(t * 23 + k);
	const hh = 1 + 0.22 * Math.sin(t * 9 + k * 2.3);
	return (
		<g transform={`translate(${f(x)} ${f(y)}) scale(${f(s * w)} ${f(s * hh)})`}>
			<path d="M -60 0 Q -80 -70 -30 -120 Q -36 -70 0 -60 Q -10 -130 30 -190 Q 30 -110 60 -90 Q 90 -50 60 0 Z" fill={c('coral-2')} />
			<path d="M -36 0 Q -50 -50 -14 -86 Q -8 -46 12 -44 Q 10 -100 34 -130 Q 40 -70 50 -40 Q 56 -14 36 0 Z" fill={c('amber-1')} />
			<path d="M -16 0 Q -20 -30 0 -54 Q 8 -30 24 -26 Q 30 -10 20 0 Z" fill={c('amber-4')} />
		</g>
	);
}

/** a door hinged at hx, swinging out toward the viewer; ghost = dashed outline only */
function Door({hx, y0, y1, w, open, dir, wood, shade, ghost}: {hx: number; y0: number; y1: number; w: number; open: number; dir: 1 | -1; wood: string; shade: string; ghost?: boolean}) {
	const th = clamp(open) * (Math.PI / 2) * 0.92;
	const ex = hx + dir * w * Math.cos(th);
	const k = 26 * Math.sin(th);
	const back = open > 0.55;
	const d = `M ${f(hx)} ${f(y0)} L ${f(ex)} ${f(y0 - k)} L ${f(ex)} ${f(y1 + k)} L ${f(hx)} ${f(y1)} Z`;
	if (ghost) return <path d={d} fill={c('bone-2')} fillOpacity={0.08} stroke={c('bone-2')} strokeWidth={7} strokeDasharray="16 10" />;
	const ix0 = hx + dir * 16 * Math.cos(th);
	const ix1 = hx + dir * (w - 16) * Math.cos(th);
	const inset = `M ${f(ix0)} ${f(y0 + 18)} L ${f(ix1)} ${f(y0 + 18 - k * 0.9)} L ${f(ix1)} ${f(y1 - 18 + k * 0.9)} L ${f(ix0)} ${f(y1 - 18)} Z`;
	return (
		<g>
			<path d={d} fill={back ? shade : wood} />
			{!back && <path d={inset} fill={shade} opacity={0.55} stroke="none" />}
			{!back && <circle cx={ex - dir * 22 * Math.cos(th)} cy={(y0 + y1) / 2} r={8} fill={K.gold} />}
		</g>
	);
}

// board on the cabinet top: perspective 8x8 between the front edge (y FRONT) and the back edge (y BACK)
const FRONT = 606;
const BACK = 540;
const BF: [number, number] = [380, 720];
const BB: [number, number] = [410, 690];
function bproj(u: number, v: number): P2 {
	const k = v / 8;
	const y = lerp(FRONT, BACK, k);
	const x0 = lerp(BF[0], BB[0], k);
	const x1 = lerp(BF[1], BB[1], k);
	return [lerp(x0, x1, u / 8), y];
}
const PIECES: [number, number, boolean][] = [
	[1, 0.5, true], [3, 1.5, true], [4, 1.5, true], [6, 0.5, true], [2, 2.5, true], [5, 3.5, true],
	[1, 7.5, false], [3, 6.5, false], [4, 5.5, false], [6, 7.5, false], [2, 6.5, false], [7, 6.5, false],
];

export const Turk: React.FC<KitComponentProps> = ({props, time}) => {
	const t = time;
	const char = clamp(track(props.char, t, 0));
	const fire = clamp(track(props.fire, t, 0));
	const dark = clamp(track(props.dark, t, 0));
	const smoke = clamp(track(props.smoke, t, 0));
	const tint = (col: string) => (char > 0 ? mixOk(col, c('ink-0'), char * 0.85) : col);
	const wood = tint(c('ochre-1'));
	const woodSh = tint(c('ochre-0'));
	const woodLt = tint(c('ochre-2'));
	const face = tint(c('amber-2'));
	const faceSh = tint(c('amber-1'));
	const brass = tint(c('amber-4'));
	const doorL = clamp(track(props.doorL, t, 0));
	const doorR = clamp(track(props.doorR, t, 0));
	const doorR2 = clamp(track(props.doorR2, t, 0));
	const drawer = clamp(track(props.drawer, t, 0));
	const candle = clamp(track(props.candle, t, 0));
	const spin = track(props.spin, t, 0);
	const tick = props.tick === true;
	const armUp = clamp(track(props.arm, t, 0));
	const reach = clamp(track(props.reach, t, 0));
	const look = track(props.look, t, 0);
	const cut = clamp(track(props.cut, t, 0));
	const xray = clamp(track(props.xray, t, 0));
	const seat = clamp(track(props.seat, t, 0));
	const lever = clamp(track(props.lever, t, 0));
	const sweepAt = when(props.sweep);
	const showPieces = props.pieces !== false;
	const turns = spin > 0 ? t * spin : 0;
	const gAng = tick ? (Math.floor(turns * 6) + easeOut(((turns * 6) % 1) * 3)) * 60 : turns * 360;

	// right arm: stiff, stepped lift (a machine), then across the board
	const stepped = (v: number) => {
		const n = 3;
		const s = v * n;
		return (Math.floor(s) + easeInOut(clamp((s % 1) * 1.4))) / n; // clockwork steps, each eased over ~5 frames
	};
	const up = armUp >= 1 || armUp <= 0 ? armUp : stepped(armUp);
	const rest: P2 = [420, 560];
	const lifted: P2 = [470, 410];
	const target = bproj(lerp(1.5, 6.5, reach), lerp(2, 5, reach));
	const sweeping = sweepAt >= 0 && t >= sweepAt;
	const sw = sweeping ? easeOut(clamp((t - sweepAt) / 0.45)) : 0;
	let hand: P2 = [lerp(rest[0], lerp(lifted[0], target[0], reach), up), lerp(rest[1], lerp(lifted[1], target[1] - 20, reach), up)];
	if (sweeping) hand = [lerp(420, 650, sw), 560 - Math.sin(sw * Math.PI) * 20];
	const sh: P2 = [372, 372];
	const el: P2 = [lerp(sh[0], hand[0], 0.5) + 30, lerp(sh[1], hand[1], 0.5) + 40 - up * 34];

	const magnets = arr<{t: number; i: number}>(props.magnets);
	const pieces = PIECES.map(([u, v, white], i) => {
		const [px, py] = bproj(u, v);
		const s = lerp(1, 0.8, v / 8);
		if (!sweeping) return {x: px, y: py, s, r: 0, o: 1, white};
		const dt = Math.max(0, t - sweepAt - 0.04 - (px - 380) / 1100);
		const vx = 560 + (i % 3) * 150;
		const vy = -560 - (i % 4) * 110;
		return {x: px + vx * dt, y: py + vy * dt + 1700 * dt * dt, s, r: dt * (320 + i * 40), o: dt > 1.0 ? 0 : 1, white};
	});

	// the hidden master lowers his hand to the lever as it engages: a pose track, so PersonBody blends it (no snap)
	const leverKeys = arr<{t: number; v: number}>(props.lever).filter((k) => typeof k.t === 'number' && typeof k.v === 'number');
	const leverOn = leverKeys.find((k) => k.v >= 0.5);
	const restPose = props.masterCandle ? 'holdHigh' : 'hold';
	const masterProps = {
		costume: 'master', face: props.masterFace ?? 'focus',
		pose: leverOn ? [{t: 0, v: restPose}, {t: Math.max(0, leverOn.t - 0.35), v: 'hold'}] : lever > 0.5 ? 'hold' : restPose,
		item: props.masterCandle ? 'candle' : 'none', seated: true, seed: 7, look: 0.5, crouch: 1,
	};
	const mx = lerp(150, 470, seat);
	const candleXY: P2 = [mx - 20 + 452 * 0.4, 609 + (236 + 170) * 0.4];

	const gears = (
		<g>
			<Gear x={200} y={700} r={52} teeth={10} rot={gAng} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
			<Gear x={290} y={765} r={44} teeth={9} rot={-gAng * 1.18 + 12} fill={tint(c('amber-4'))} shade={tint(c('amber-2'))} />
			<Gear x={330} y={680} r={30} teeth={7} rot={gAng * 1.7} fill={tint(c('ochre-2'))} shade={tint(c('ochre-0'))} />
			<Gear x={180} y={790} r={24} teeth={6} rot={-gAng * 2.1} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
		</g>
	);

	return (
		<svg viewBox="0 0 900 1000" width="100%" height="100%" preserveAspectRatio="xMidYMax meet" style={{overflow: 'visible'}}>
			<g {...inkG(props.ink)}>
			<ellipse cx={450} cy={972} rx={400} ry={24} fill={c('ink-1')} opacity={0.25} stroke="none" />
			{/* the automaton, seated behind the cabinet top */}
			<g>
				<path d="M 236 552 L 120 330" stroke={woodSh} strokeWidth={12} strokeLinecap="round" />
				<path d="M 96 300 Q 92 350 124 352 Q 150 350 150 312 Z" fill={tint(c('ochre-0'))} />
				<path d="M 214 360 Q 300 320 386 360 L 410 590 L 190 590 Z" fill={tint(c('coral-2'))} />
				<path d="M 300 334 Q 352 336 386 360 L 410 590 L 318 590 Z" fill={tint(c('coral-0'))} />
				<path d="M 250 380 L 350 380 L 340 410 L 260 410 Z" fill={tint(c('amber-4'))} />
				<path d="M 228 382 L 196 476 L 236 548" stroke={tint(c('coral-1'))} strokeWidth={40} strokeLinecap="round" strokeLinejoin="round" fill="none" />
				<circle cx={196} cy={476} r={14} fill={brass} />
				<circle cx={236} cy={550} r={22} fill={woodLt} />
				<ellipse cx={300} cy={346} rx={96} ry={30} fill={tint(c('ochre-3'))} />
				<ellipse cx={330} cy={352} rx={60} ry={20} fill={tint(c('ochre-2'))} />
				<rect x={276} y={316} width={48} height={26} rx={6} fill={brass} />
				{/* carved wooden head: hinged jaw seam, painted stare */}
				<ellipse cx={300} cy={262} rx={74} ry={84} fill={faceSh} />
				<ellipse cx={292} cy={254} rx={68} ry={78} fill={face} />
				<path d="M 236 286 L 252 330 Q 300 348 348 330 L 364 286" stroke={faceSh} strokeWidth={6} fill="none" strokeLinejoin="round" />
				<circle cx={238} cy={284} r={6} fill={brass} />
				<circle cx={362} cy={284} r={6} fill={brass} />
				{[272, 332].map((x, i) => (
					<g key={i}>
						<ellipse cx={x} cy={240} rx={18} ry={14} fill={tint(c('bone-2'))} />
						<circle cx={x + 3 + look * 8} cy={241} r={8} fill={tint(c('ink-1'))} />
						<rect x={x - 22} y={214} width={44} height={9} rx={2} fill={tint(c('ink-1'))} />
					</g>
				))}
				<path d="M 240 300 Q 270 282 300 292 Q 330 282 360 300 Q 340 310 300 302 Q 260 310 240 300 Z" fill={tint(c('ink-1'))} />
				<path d="M 270 316 Q 300 328 330 316 L 300 372 Z" fill={tint(c('ink-1'))} />
				<g transform="translate(0 -26)">
					<ellipse cx={300} cy={180} rx={110} ry={74} fill={tint(c('bone-1'))} />
					<path d="M 300 108 Q 392 112 410 180 Q 380 238 300 248 Q 360 210 360 170 Q 352 128 300 108 Z" fill={tint(c('bone-0'))} />
					<path d="M 196 196 Q 300 250 404 196 L 400 218 Q 300 270 200 218 Z" fill={tint(c('coral-2'))} />
					<circle cx={300} cy={176} r={16} fill={tint(c('magenta-2'))} />
					<path d="M 300 162 Q 318 92 352 72 Q 334 120 312 166 Z" fill={tint(c('violet-2'))} />
				</g>
			</g>
			{/* cabinet top with the board */}
			<path d={`M 102 ${FRONT + 6} L 798 ${FRONT + 6} L 760 ${BACK - 4} L 140 ${BACK - 4} Z`} fill={wood} />
			<rect x={102} y={FRONT + 4} width={696} height={22} rx={5} fill={woodLt} />
			{Array.from({length: 64}, (_, i) => {
				const u = i % 8;
				const v = Math.floor(i / 8);
				const a = bproj(u, v);
				const b = bproj(u + 1, v);
				const cc = bproj(u + 1, v + 1);
				const d = bproj(u, v + 1);
				return <path key={i} d={`M ${f(a[0])} ${f(a[1])} L ${f(b[0])} ${f(b[1])} L ${f(cc[0])} ${f(cc[1])} L ${f(d[0])} ${f(d[1])} Z`}
					fill={(u + v) % 2 ? tint(c('bone-1')) : tint(c('ink-2'))} stroke="none" />;
			})}
			{showPieces &&
				pieces.map((p, i) =>
					p.o > 0 ? (
						<g key={i} transform={`translate(${f(p.x)} ${f(p.y)}) scale(${f(p.s)}) rotate(${f(p.r)} 0 -14)`}>
							<path d="M -11 0 L 11 0 L 7 -18 Q 0 -24 -7 -18 Z" fill={p.white ? c('bone-2') : c('ink-0')} />
							<circle cy={-26} r={8} fill={p.white ? c('bone-2') : c('ink-0')} />
						</g>
					) : null,
				)}
			{/* right arm over the board */}
			<path d={`M ${sh[0]} ${sh[1]} L ${f(el[0])} ${f(el[1])} L ${f(hand[0])} ${f(hand[1])}`} stroke={tint(c('coral-1'))} strokeWidth={40}
				strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<circle cx={sh[0]} cy={sh[1]} r={16} fill={brass} />
			<circle cx={el[0]} cy={el[1]} r={15} fill={brass} />
			<path d={`M ${f(hand[0] - 26)} ${f(hand[1] - 4)} q 26 -22 52 0 l -6 22 q -20 8 -40 0 Z`} fill={woodLt} />
			{[-16, -4, 8].map((dx, i) => (
				<rect key={i} x={hand[0] + dx} y={hand[1] + 10} width={10} height={20} rx={5} fill={woodLt} />
			))}
			{/* front */}
			<rect x={120} y={FRONT + 26} width={660} height={268} fill={wood} />
			<rect x={600} y={FRONT + 26} width={180} height={268} fill={woodSh} opacity={0.6} stroke="none" />
			{/* compartments */}
			<g>
				<rect x={140} y={642} width={240} height={180} fill={tint(c('ink-0'))} />
				<rect x={400} y={642} width={360} height={180} fill={tint(c('ink-1'))} />
				{candle > 0 && (
					<g opacity={candle} stroke="none">
						{/* the candle is held into the left bay: the light pools there and spills into the right one */}
						<rect x={140} y={642} width={240} height={180} fill={c('amber-3')} opacity={0.42} />
						<circle cx={260} cy={735} r={110} fill={c('amber-4')} opacity={0.35} />
						<rect x={400} y={642} width={360} height={180} fill={c('amber-3')} opacity={0.16} />
					</g>
				)}
				{cut <= 0 && gears}
				{/* right side: a brass drum and small gears (machinery, no room for a person, it seems) */}
				{cut <= 0 && (
					<g>
						<rect x={470} y={660} width={8} height={150} fill={tint(c('amber-2'))} />
						<rect x={680} y={660} width={8} height={150} fill={tint(c('amber-2'))} />
						<rect x={474} y={724} width={210} height={8} fill={tint(c('amber-2'))} />
						<Gear x={560} y={700} r={40} teeth={9} rot={-gAng * 1.2} fill={tint(c('amber-4'))} shade={tint(c('amber-2'))} />
						<Gear x={636} y={770} r={34} teeth={8} rot={gAng * 1.4 + 10} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
						<Gear x={720} y={690} r={26} teeth={7} rot={-gAng * 1.9} fill={tint(c('ochre-2'))} shade={tint(c('ochre-0'))} />
						<Gear x={440} y={780} r={24} teeth={6} rot={gAng * 1.6} fill={tint(c('amber-3'))} shade={tint(c('amber-1'))} />
					</g>
				)}
				{cut > 0 && (
					<g opacity={clamp(cut * 1.6)}>
						{/* board underside: iron markers on threads under the squares */}
						<rect x={140} y={642} width={620} height={10} fill={c('ochre-0')} />
						{Array.from({length: 8}, (_, i) => {
							const x = 420 + i * 40;
							const hit = magnets.filter((m) => typeof m.t === 'number' && m.i === i && t >= m.t).pop();
							const age = hit ? t - hit.t : 9;
							const upm = hit ? (age < 0.18 ? easeOut(age / 0.18) : 1 - clamp((age - 1.4) / 0.4)) : 0;
							const y = 700 - upm * 44;
							return (
								<g key={i}>
									<path d={`M ${f(x)} 650 V ${f(y)}`} stroke={c('bone-0')} strokeWidth={3} />
									{upm > 0.05 && <circle cx={x} cy={y} r={26} fill={c('coral-3')} opacity={0.5 * upm} stroke="none" />}
									<circle cx={x} cy={y} r={14} fill={upm > 0.05 ? c('coral-2') : c('sky-3')} />
								</g>
							);
						})}
						<rect x={140} y={822} width={620} height={66} fill={c('ink-1')} />
						<rect x={140} y={876} width={620} height={10} fill={c('amber-2')} />
						<rect x={mx + 40} y={862} width={170} height={16} rx={8} fill={c('coral-1')} />
						{lever > 0 && (
							<g opacity={lever}>
								<path d={`M ${f(mx + 160)} 790 L ${f(mx + 210)} 680 L 372 ${FRONT} L ${f(sh[0])} ${f(sh[1] + 40)}`} stroke={c('amber-3')}
									strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" fill="none" />
								<circle cx={mx + 210} cy={680} r={10} fill={c('amber-1')} />
							</g>
						)}
						{dark > 0 && <rect x={140} y={642} width={620} height={246} fill={c('ink-0')} opacity={0.6 * dark} stroke="none" />}
						{xray > 0 && (
							<g opacity={xray}>
								<Door hx={140} y0={642} y1={822} w={240} open={doorL} dir={1} wood={wood} shade={woodSh} ghost />
								<Door hx={400} y0={642} y1={822} w={180} open={doorR} dir={1} wood={wood} shade={woodSh} ghost />
								<Door hx={760} y0={642} y1={822} w={180} open={doorR2} dir={-1} wood={wood} shade={woodSh} ghost />
							</g>
						)}
						{props.masterCandle === true && (
							<circle cx={candleXY[0]} cy={candleXY[1]} r={95 + 6 * Math.sin(t * 9)} fill={c('amber-4')} opacity={0.18 + 0.3 * dark} stroke="none" />
						)}
						<g transform={`translate(${f(mx - 20)} 609) scale(0.4)`}>
							<PersonBody props={masterProps} t={t} />
						</g>
						{/* the false gear panel: in front of him when he slides left */}
						<rect x={140} y={642} width={244} height={246} fill={c('ink-1')} opacity={0.62} stroke="none" />
						{gears}
						<path d="M 384 644 V 886" stroke={c('amber-4')} strokeWidth={6} strokeDasharray="14 10" />
					</g>
				)}
			</g>
			{/* doors and drawer: solid on the outside view, dashed ghosts on the cutaway */}
			{cut < 1 && (
				<g opacity={1 - clamp(cut * 2)}>
					<Door hx={140} y0={642} y1={822} w={240} open={doorL} dir={1} wood={wood} shade={woodSh} />
					<Door hx={400} y0={642} y1={822} w={180} open={doorR} dir={1} wood={wood} shade={woodSh} />
					<Door hx={760} y0={642} y1={822} w={180} open={doorR2} dir={-1} wood={wood} shade={woodSh} />
				</g>
			)}
			<g opacity={1 - clamp(cut * 2)}>
				<rect x={140} y={838 + drawer * 40} width={620} height={48} rx={4} fill={woodSh} />
				<rect x={146} y={844 + drawer * 40} width={608} height={36} rx={4} fill={wood} />
				<circle cx={450} cy={862 + drawer * 40} r={8} fill={K.gold} />
			</g>
			<rect x={110} y={894} width={680} height={24} rx={6} fill={woodSh} />
			{[160, 360, 540, 740].map((x) => (
				<g key={x}>
					<rect x={x - 8} y={916} width={16} height={22} fill={woodSh} />
					<circle cx={x} cy={950} r={20} fill={tint(c('ink-1'))} />
					<circle cx={x} cy={950} r={7} fill={K.gold} />
				</g>
			))}
			{smoke > 0 && (
				<g stroke="none">
					{cut > 0.5 && (
						<path d={`M ${f(candleXY[0])} ${f(candleXY[1] - 40)} C ${f(candleXY[0] + 10)} 600 430 560 420 470 S 410 360 404 330`}
							fill="none" stroke={c('bone-1')} strokeWidth={9} strokeDasharray="4 22" strokeLinecap="round"
							strokeDashoffset={-t * 60} opacity={0.85 * smoke} />
					)}
					{[0, 1, 2, 3, 4].map((i) => {
						const age = (t * 0.55 + i / 5) % 1;
						const x = 300 + Math.sin((t + i) * 2.1) * 14 + age * 40 * (i % 2 ? 1 : -1);
						const y = 70 - age * 230;
						return <circle key={i} cx={f(x)} cy={f(y)} r={f(14 + age * 34)} fill={c('bone-0')} opacity={smoke * 0.7 * (1 - age)} />;
					})}
				</g>
			)}
			{fire > 0 &&
				[[200, 600], [460, 430], [620, 600], [150, 330], [520, 880], [760, 700]].map(([x, y], i) => (
					<Flame key={i} x={x} y={y} s={(0.9 + (i % 3) * 0.35) * clamp(fire * 1.5 - i * 0.08)} t={t} k={i} />
				))}
			</g>
		</svg>
	);
};
