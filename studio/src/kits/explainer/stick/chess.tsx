/**
 * stick/Chess: a chessboard close-up seen from the player's side (perspective trapezoid), 1000 x 800 box.
 *
 * props
 *   moves     [{t, from: "e2", to: "e4", dur?: 0.5, hand?: "turk" | "human" | "none", side?: "far" | "near"}]
 *             a piece hops from square to square; a hand carries it (turk = carved wooden hand from the far side,
 *             human = a bone-white round hand from the near side)
 *   sweepAt   the wooden arm sweeps every piece off the board
 *   setup     "mid" (default) | "start"
 *   glow      square name to ring (e.g. the king in check), with glowAt
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {arr, clamp, easeInOut, easeOut, lerp, num, str} from '../util';
import {c, f, inkG, step} from './common';
import {when} from './turk';

type P2 = [number, number];
const BACK_Y = 170;
const FRONT_Y = 760;
const BACK = [230, 770];
const FRONT = [30, 970];

/** board coords (u, v in 0..8, v = 0 at the near edge) -> screen point and scale */
function proj(u: number, v: number): {p: P2; s: number} {
	const k = v / 8;
	// perspective: rows get thinner toward the back
	const yk = 1 - Math.pow(1 - k, 1.25);
	const y = lerp(FRONT_Y, BACK_Y, yk);
	const x0 = lerp(FRONT[0], BACK[0], yk);
	const x1 = lerp(FRONT[1], BACK[1], yk);
	return {p: [lerp(x0, x1, u / 8), y], s: lerp(1, 0.62, yk)};
}

const sqUV = (sq: string): [number, number] => [sq.charCodeAt(0) - 97 + 0.5, parseInt(sq[1], 10) - 0.5];

const SETUPS: Record<string, Record<string, string>> = {
	mid: {e4: 'wP', d4: 'wP', f3: 'wN', c4: 'wB', e1: 'wK', a2: 'wP', h2: 'wR', d1: 'wQ',
		e5: 'bP', d6: 'bP', c6: 'bN', g8: 'bK', f7: 'bP', a7: 'bP', h8: 'bR', d8: 'bQ', g6: 'bP'},
	start: {},
	napoleon: {e4: 'wP', c3: 'wN', d1: 'wQ', e1: 'wK', b2: 'wP', g2: 'wP', f1: 'wB', h1: 'wR',
		e5: 'bP', c5: 'bP', f6: 'bN', e8: 'bK', d8: 'bQ', a7: 'bP', g7: 'bP', h8: 'bR'},
};

function Piece({kind, white, x, y, s, rot = 0}: {kind: string; white: boolean; x: number; y: number; s: number; rot?: number}) {
	const fill = white ? c('bone-2') : c('ink-1');
	const sh = white ? c('bone-0') : c('ink-0');
	const k = kind;
	let body = '';
	let head: React.ReactNode = null;
	if (k === 'P') {
		body = 'M -26 0 L 26 0 L 18 -14 L 10 -40 L -10 -40 L -18 -14 Z';
		head = <circle cy={-54} r={17} fill={fill} />;
	} else if (k === 'R') {
		body = 'M -28 0 L 28 0 L 22 -14 L 20 -62 L 26 -62 L 26 -84 L 14 -84 L 14 -74 L 6 -74 L 6 -84 L -6 -84 L -6 -74 L -14 -74 L -14 -84 L -26 -84 L -26 -62 L -20 -62 L -22 -14 Z';
	} else if (k === 'N') {
		body = 'M -28 0 L 28 0 L 22 -14 L 18 -50 Q 24 -80 4 -96 L -6 -86 L -30 -66 L -24 -54 L -8 -60 L -18 -14 Z';
	} else if (k === 'B') {
		body = 'M -26 0 L 26 0 L 18 -14 L 12 -50 Q 22 -72 0 -96 Q -22 -72 -12 -50 L -18 -14 Z';
		head = <circle cy={-102} r={7} fill={fill} />;
	} else if (k === 'Q') {
		body = 'M -28 0 L 28 0 L 20 -14 L 14 -66 L 26 -96 L 12 -82 L 0 -104 L -12 -82 L -26 -96 L -14 -66 L -20 -14 Z';
	} else {
		body = 'M -28 0 L 28 0 L 20 -14 L 14 -70 L 22 -84 L -22 -84 L -14 -70 L -20 -14 Z';
		head = <path d="M -5 -84 V -112 M -14 -102 H 14" stroke={fill} strokeWidth={8} strokeLinecap="round" />;
	}
	return (
		<g transform={`translate(${f(x)} ${f(y)}) scale(${f(s)}) rotate(${f(rot)} 0 -40)`}>
			<ellipse cx={4} cy={2} rx={32} ry={9} fill={c('ink-0')} opacity={0.3} stroke="none" />
			<path d={body} fill={fill} />
			<path d={body} fill={sh} clipPath="url(#stick-rhalf)" />
			{head}
		</g>
	);
}

function TurkHand({x, y, s}: {x: number; y: number; s: number}) {
	return (
		<g transform={`translate(${f(x)} ${f(y)}) scale(${f(s)}) rotate(38)`}>
			<path d="M -40 -1100 L 30 -1100 L 34 -110 L -36 -110 Z" fill={c('coral-1')} />
			<path d="M 0 -1100 L 30 -1100 L 34 -110 L 2 -110 Z" fill={c('coral-0')} />
			<rect x={-46} y={-130} width={86} height={34} rx={14} fill={c('ochre-3')} />
			<path d="M -38 -98 Q -44 -40 -20 -24 L 26 -24 Q 44 -50 36 -98 Z" fill={c('ochre-2')} />
			<path d="M 6 -98 L 36 -98 Q 44 -50 26 -24 L 8 -24 Z" fill={c('ochre-1')} />
			{[-24, -8, 8, 24].map((dx, i) => (
				<rect key={i} x={dx - 6} y={-34} width={12} height={34} rx={6} fill={i > 1 ? c('ochre-1') : c('ochre-2')} />
			))}
		</g>
	);
}

function HumanHand({x, y, s}: {x: number; y: number; s: number}) {
	return (
		<g transform={`translate(${f(x)} ${f(y)}) scale(${f(s)}) rotate(-34)`}>
			<path d="M -34 1100 L 34 1100 L 30 70 L -30 70 Z" fill={c('dusk-1')} />
			<rect x={-40} y={60} width={80} height={30} rx={12} fill={c('bone-2')} />
			<circle cx={0} cy={36} r={36} fill={c('bone-1')} />
			<circle cx={8} cy={42} r={26} fill={c('bone-0')} />
			<circle cx={-6} cy={4} r={14} fill={c('bone-1')} />
			<circle cx={14} cy={8} r={13} fill={c('bone-1')} />
		</g>
	);
}

export const Chess: React.FC<KitComponentProps> = ({props, time}) => {
	const t = time;
	const setup = {...(SETUPS[str(props.setup, 'mid')] ?? SETUPS.mid)};
	const moves = arr<{t: number; from: string; to: string; dur?: number; hand?: string; illegal?: boolean}>(props.moves)
		.filter((m) => typeof m.t === 'number')
		.sort((a, b) => a.t - b.t);
	// board state at time t. Each move: the hand travels in from off-board over LEAD s, carries the piece for dur s, then
	// leaves over OUT s; hands of consecutive moves may overlap (one leaves while the next arrives), pieces never pop.
	const LEAD = 0.3;
	const OUT = 0.35;
	const pos: Record<string, string> = {...setup};
	const flying: {kind: string; a: P2; b: P2; k: number; s0: number; s1: number}[] = [];
	const hands: {hand: string; x: number; y: number; s: number; o: number}[] = [];
	let illegal: {a: P2; b: P2; age: number} | null = null;
	for (const m of moves) {
		const dur = m.dur ?? 0.55;
		if (t < m.t - LEAD) break;
		const piece = pos[m.from];
		if (!piece) continue;
		const A = proj(...sqUV(m.from));
		const B = proj(...sqUV(m.to));
		const k = clamp((t - m.t) / dur);
		if (m.illegal && t >= m.t + dur && t < m.t + dur + 1.2) {
			illegal = {a: A.p, b: B.p, age: t - m.t - dur};
		}
		if (t >= m.t + dur) {
			delete pos[m.from];
			pos[m.to] = piece; // it lands at the end of the move
		} else if (t >= m.t) {
			delete pos[m.from];
			flying.push({kind: piece, a: A.p, b: B.p, k, s0: A.s, s1: B.s});
		}
		if ((m.hand === 'turk' || m.hand === 'human') && t < m.t + dur + OUT) {
			const e = easeInOut(k);
			const kin = clamp((t - m.t + LEAD) / LEAD);
			const out = clamp((t - m.t - dur) / OUT);
			hands.push({hand: m.hand, x: lerp(A.p[0], B.p[0], e), y: lerp(A.p[1], B.p[1], e) - Math.sin(e * Math.PI) * 120,
				s: lerp(A.s, B.s, e), o: Math.max(easeInOut(out), 1 - easeInOut(kin))});
		}
	}
	const sweepAt = when(props.sweep);
	const topple = arr<{t: number; v: string}>(props.topple).filter((x) => typeof x.t === 'number');
	const sweeping = sweepAt >= 0 && t >= sweepAt;
	const sw = sweeping ? clamp((t - sweepAt) / 0.5) : 0;
	const armX = lerp(-200, 1250, easeInOut(sw));

	const squares: React.ReactNode[] = [];
	for (let v = 7; v >= 0; v--)
		for (let u = 0; u < 8; u++) {
			const a = proj(u, v).p;
			const b = proj(u + 1, v).p;
			const cc = proj(u + 1, v + 1).p;
			const d = proj(u, v + 1).p;
			squares.push(
				<path key={`${u}${v}`} d={`M ${f(a[0])} ${f(a[1])} L ${f(b[0])} ${f(b[1])} L ${f(cc[0])} ${f(cc[1])} L ${f(d[0])} ${f(d[1])} Z`}
					fill={(u + v) % 2 === 0 ? c('ink-2') : c('bone-1')} stroke="none" />,
			);
		}
	const glowSq = step<string>(props.glow, t, '');
	const glowAt = arr<{t: number}>(props.glow).length ? (arr<{t: number}>(props.glow)[0].t ?? 0) : 0;
	const items = Object.entries(pos)
		.map(([sq, p]) => {
			const pr = proj(...sqUV(sq));
			let x = pr.p[0];
			let y = pr.p[1];
			let rot = 0;
			let gone = false;
			if (sweeping) {
				const delay = (x + 200) / 1450;
				const dt = Math.max(0, (t - sweepAt) - delay * 0.5);
				if (dt > 0) {
					x += 900 * dt + (y - 400) * 0.2 * dt;
					y += -700 * dt + 2400 * dt * dt;
					rot = dt * 520;
					gone = dt > 1.2;
				}
			}
			const tp = topple.find((q) => q.v === sq && t >= q.t);
			if (tp && !sweeping) rot = 82 * easeOut(clamp((t - tp.t) / 0.35));
			return {sq, p, x, y, s: pr.s, rot, gone};
		})
		.sort((a, b) => a.y - b.y);
	const mv = flying.map((p, i) => {
		const e = easeInOut(p.k);
		return <Piece key={`fly${i}`} kind={p.kind[1]} white={p.kind[0] === 'w'} x={lerp(p.a[0], p.b[0], e)}
			y={lerp(p.a[1], p.b[1], e) - Math.sin(e * Math.PI) * 120} s={lerp(p.s0, p.s1, e)} />;
	});
	const handNode = hands.map((h, i) =>
		h.hand === 'turk' ? <TurkHand key={`h${i}`} x={h.x + h.o * 620} y={h.y - 96 * h.s - h.o * 760} s={h.s * 1.1} />
			: <HumanHand key={`h${i}`} x={h.x + 10 - h.o * 420} y={h.y - 40 * h.s + h.o * 950} s={h.s * 1.1} />);
	return (
		<svg viewBox="0 0 1000 800" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" style={{overflow: 'visible'}}>
			<defs>
				<clipPath id="stick-rhalf" clipPathUnits="userSpaceOnUse">
					<rect x={4} y={-300} width={200} height={600} />
				</clipPath>
			</defs>
			<g {...inkG(props.ink)}>
			{props.bg !== false && (
				<g stroke="none">
					<rect x={-700} y={-1300} width={2400} height={3400} fill={c(str(props.room, 'violet-0'))} />
					<rect x={-700} y={FRONT_Y + 40} width={2400} height={1400} fill={c('ochre-0')} />
					<rect x={-700} y={FRONT_Y + 40} width={2400} height={40} fill={c('ochre-1')} />
				</g>
			)}
			{/* board frame */}
			<path d={`M ${FRONT[0] - 26} ${FRONT_Y + 30} L ${FRONT[1] + 26} ${FRONT_Y + 30} L ${BACK[1] + 16} ${BACK_Y - 16} L ${BACK[0] - 16} ${BACK_Y - 16} Z`} fill={c('ochre-1')} />
			<path d={`M ${FRONT[0] - 26} ${FRONT_Y + 30} L ${FRONT[1] + 26} ${FRONT_Y + 30} L ${FRONT[1] + 26} ${FRONT_Y + 64} L ${FRONT[0] - 26} ${FRONT_Y + 64} Z`} fill={c('ochre-0')} />
			{squares}
			{glowSq && t >= glowAt && (() => {
				const pr = proj(...sqUV(glowSq));
				const k = easeOut(clamp((t - glowAt) / 0.3));
				return <ellipse cx={pr.p[0]} cy={pr.p[1]} rx={70 * pr.s * k} ry={26 * pr.s * k} fill="none" stroke={c('coral-2')} strokeWidth={8} />;
			})()}
			{items.map((it) => (it.gone ? null : <Piece key={it.sq} kind={it.p[1]} white={it.p[0] === 'w'} x={it.x} y={it.y} s={it.s} rot={it.rot} />))}
			{illegal && (() => {
				const k = easeOut(clamp(illegal.age / 0.25));
				const mxp = (illegal.a[0] + illegal.b[0]) / 2;
				const myp = (illegal.a[1] + illegal.b[1]) / 2 - 60;
				return (
					<g opacity={illegal.age > 0.9 ? 1 - clamp((illegal.age - 0.9) / 0.3) : 1}>
						<path d={`M ${f(illegal.a[0])} ${f(illegal.a[1])} Q ${f(mxp)} ${f(myp - 80)} ${f(illegal.b[0])} ${f(illegal.b[1])}`} fill="none"
							stroke={c('coral-2')} strokeWidth={12} strokeDasharray="22 14" strokeLinecap="round" />
						<g transform={`translate(${f(illegal.b[0] + 70)} ${f(illegal.b[1] - 150)}) scale(${f(k * 0.8)})`}>
							<circle r={58} fill={c('coral-2')} />
							<path d="M -24 -24 L 24 24 M 24 -24 L -24 24" stroke={c('bone-2')} strokeWidth={14} strokeLinecap="round" />
						</g>
					</g>
				);
			})()}
			{mv}
			{handNode}
			{sweeping && sw < 1 && (
				<g transform={`translate(${f(armX)} 470) rotate(-8)`}>
					<rect x={-760} y={-60} width={720} height={120} rx={60} fill={c('coral-1')} />
					<rect x={-760} y={-60} width={720} height={50} rx={25} fill={c('coral-2')} />
					<rect x={-70} y={-70} width={60} height={140} rx={24} fill={c('ochre-3')} />
					<path d="M -20 -60 Q 90 -70 120 0 Q 90 70 -20 60 Z" fill={c('ochre-2')} />
				</g>
			)}
			</g>
		</svg>
	);
};
