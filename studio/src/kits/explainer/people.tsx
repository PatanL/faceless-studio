/**
 * People and everyday scale objects: scuba diver (swim cycle), filled-silhouette YOU (style "stick" = line figure),
 * city bus, car, elephant. Facing RIGHT.
 */
import React from 'react';
import {paint, type DrawCtx, type Figure} from './figure';
import {bool, num, rnd, str, type Pt} from './util';

const rad = (d: number) => (d * Math.PI) / 180;
const polar = (p: Pt, a: number, l: number): Pt => [p[0] + Math.cos(rad(a)) * l, p[1] + Math.sin(rad(a)) * l];

// ================================================================ diver

function legPose(t: number, phase: number, kick: number) {
	const s = Math.sin(t + phase);
	const thigh = 180 + 9 * kick * s;
	const knee = 10 + 12 * kick * (0.5 + 0.5 * Math.sin(t + phase + 1.1));
	const ankle = 8 - 22 * kick * Math.sin(t + phase - 0.9); // fin lags the shin
	return {thigh, knee, ankle};
}

const Leg: React.FC<{c: DrawCtx; hip: Pt; t: number; phase: number; kick: number; suit: string; fin: string; finEdge: string}> = ({
	c,
	hip,
	t,
	phase,
	kick,
	suit,
	fin,
	finEdge,
}) => {
	const {thigh, knee, ankle} = legPose(t, phase, kick);
	const kneeP = polar(hip, thigh, 104);
	const shinA = thigh + knee;
	const ankleP = polar(kneeP, shinA, 98);
	const finA = shinA + ankle;
	// fin: a tapered blade from the ankle
	const n = finA + 90;
	const base1 = polar(ankleP, n, 12);
	const base2 = polar(ankleP, n, -12);
	const tip = polar(ankleP, finA, 128);
	const tip1 = polar(tip, n, 30);
	const tip2 = polar(tip, n, -30);
	const notch = polar(ankleP, finA, 112);
	return (
		<g>
			<path
				d={`M ${base1[0]} ${base1[1]} L ${tip1[0]} ${tip1[1]} L ${notch[0]} ${notch[1]} L ${tip2[0]} ${tip2[1]} L ${base2[0]} ${base2[1]} Z`}
				fill={paint(c, fin)}
				stroke={paint(c, finEdge)}
				strokeWidth={3}
				strokeLinejoin="round"
			/>
			<path d={`M ${hip[0]} ${hip[1]} L ${kneeP[0]} ${kneeP[1]} L ${ankleP[0]} ${ankleP[1]}`} stroke={paint(c, suit)} strokeWidth={30} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<path d={`M ${hip[0]} ${hip[1]} L ${kneeP[0]} ${kneeP[1]}`} stroke={paint(c, suit)} strokeWidth={36} strokeLinecap="round" fill="none" />
		</g>
	);
};

const diverDraw = (c: DrawCtx) => {
	const speed = c.speed;
	const kick = c.idle ? num(c.p.kick, 1) * c.amp : 0;
	const tt = c.t * Math.PI * 2 * 1.1 * speed;
	const suit = str(c.p.suit, '#15181c');
	const fin = str(c.p.fins, '#f5c02e');
	const arms = str(c.p.arms, 'forward');
	const torch = bool(c.p.torch, false);
	const bubbles = bool(c.p.bubbles, true);
	const bob = c.idle ? Math.sin(tt * 0.5) * 3 : 0;
	const hip: Pt = [220, 112 + bob * 0.4];
	const sh: Pt = [418, 106 + bob];
	const armSwing = c.idle ? Math.sin(tt * 0.5) * 4 : 0;
	const upperA = arms === 'forward' ? -6 + armSwing : 172 + armSwing;
	const elbow = polar(sh, upperA, 74);
	const foreA = arms === 'forward' ? 2 + armSwing : 178;
	const hand = polar(elbow, foreA, 70);
	const beamLen = num(c.p.beam, 760);
	const bubbleEls: React.ReactNode[] = [];
	if (bubbles && !c.sil) {
		for (let i = 0; i < 9; i++) {
			const period = 1.6;
			const life = (c.t + rnd(`db${i}`) * period * 3) % (period * 1.5);
			const x = 506 + Math.sin(life * 5 + i) * 7 + life * 14;
			const y = 112 - life * 120;
			const r = 3 + rnd(`dbr${i}`) * 5 + life * 2;
			bubbleEls.push(<circle key={i} cx={x} cy={y} r={r} fill="none" stroke="rgba(210,245,255,0.75)" strokeWidth={2} opacity={1 - life / (period * 1.5)} />);
		}
	}
	return (
		<g>
			<defs>
				<linearGradient id={`${c.id}-beam`} x1="0" y1="0" x2="1" y2="0">
					<stop offset="0" stopColor="#fff8d8" stopOpacity={0.55} />
					<stop offset="1" stopColor="#fff8d8" stopOpacity={0} />
				</linearGradient>
				<linearGradient id={`${c.id}-tank`} x1="0" y1="0" x2="0" y2="1">
					<stop offset="0" stopColor={paint(c, '#f4f6f7')} />
					<stop offset="1" stopColor={paint(c, '#a9b1b6')} />
				</linearGradient>
			</defs>
			{torch && !c.sil ? (
				<path d={`M ${hand[0] + 20} ${hand[1] - 6} L ${hand[0] + beamLen} ${hand[1] - beamLen * 0.22} L ${hand[0] + beamLen} ${hand[1] + beamLen * 0.22} L ${hand[0] + 20} ${hand[1] + 6} Z`} fill={`url(#${c.id}-beam)`} />
			) : null}
			{/* far arm + far leg */}
			<path d={`M ${sh[0] - 10} ${sh[1] + 6} L ${elbow[0] - 8} ${elbow[1] + 10} L ${hand[0] - 14} ${hand[1] + 12}`} stroke={paint(c, '#0b0d10')} strokeWidth={22} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			<Leg c={c} hip={[hip[0], hip[1] + 4]} t={tt} phase={Math.PI} kick={kick} suit="#0b0d10" fin="#c9961c" finEdge="#9c7310" />
			<Leg c={c} hip={hip} t={tt} phase={0} kick={kick} suit={suit} fin={fin} finEdge="#c9961c" />
			{/* torso */}
			<path d={`M 200 ${96 + bob * 0.4} C 260 ${86 + bob * 0.6} 360 ${82 + bob} 424 ${88 + bob} C 446 ${92 + bob} 452 ${118 + bob} 432 ${126 + bob} C 360 ${134 + bob} 260 ${134 + bob * 0.6} 200 ${128 + bob * 0.4} C 184 ${122 + bob * 0.4} 184 ${102 + bob * 0.4} 200 ${96 + bob * 0.4} Z`} fill={paint(c, suit)} />
			{c.sil ? null : <path d={`M 230 ${120 + bob * 0.5} C 300 ${126 + bob} 380 ${124 + bob} 430 ${118 + bob}`} stroke="#2b3138" strokeWidth={4} fill="none" opacity={0.8} />}
			{/* tank + strap */}
			<g transform={`translate(0 ${bob})`}>
				<rect x={252} y={58} width={158} height={32} rx={16} fill={`url(#${c.id}-tank)`} />
				{c.sil ? null : <rect x={300} y={58} width={10} height={32} fill="#7f888e" opacity={0.6} />}
				<rect x={406} y={66} width={16} height={14} rx={3} fill={paint(c, '#6d757b')} />
				<rect x={334} y={84} width={14} height={40} rx={4} fill={paint(c, '#2a3036')} />
				{c.sil ? null : <path d="M 420 74 C 450 70 470 90 494 112" stroke="#3a4248" strokeWidth={5} fill="none" strokeLinecap="round" />}
			</g>
			{/* head */}
			<g transform={`translate(0 ${bob})`}>
				<circle cx={470} cy={100} r={28} fill={paint(c, suit)} />
				<rect x={478} y={84} width={30} height={24} rx={8} fill={paint(c, '#0a0c0e')} />
				{c.sil ? null : <rect x={483} y={88} width={21} height={16} rx={5} fill="#6fd6e8" />}
				{c.sil ? null : <path d="M 487 91 L 494 91" stroke="#e8fbff" strokeWidth={3} strokeLinecap="round" />}
				<circle cx={498} cy={116} r={8} fill={paint(c, '#8a9196')} />
			</g>
			{/* near arm */}
			<path d={`M ${sh[0]} ${sh[1]} L ${elbow[0]} ${elbow[1]} L ${hand[0]} ${hand[1]}`} stroke={paint(c, suit)} strokeWidth={24} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			{torch ? (
				<g transform={`translate(${hand[0]} ${hand[1]}) rotate(${foreA})`}>
					<rect x={-4} y={-9} width={34} height={18} rx={5} fill={paint(c, '#2b3136')} />
					<rect x={26} y={-11} width={8} height={22} rx={3} fill={paint(c, '#fff3c4')} />
				</g>
			) : (
				<circle cx={hand[0]} cy={hand[1]} r={10} fill={paint(c, '#d8dde0')} />
			)}
			{bubbleEls}
		</g>
	);
};

const diver: Figure = {label: 'DIVER', box: [-115, 50, 690, 120], size: 2.6, axis: 'w', draw: diverDraw};

// ================================================================ stick figure YOU

const youDraw = (c: DrawCtx) => {
	// style "diver": the hook diver's palette standing upright (black suit, light rim, mask, #d8d8d8 tank, yellow fins)
	const dv = str(c.p.style, 'filled') === 'diver';
	const col = paint(c, dv ? '#15181c' : str(c.p.color, '#f3f6f7'));
	const pose = str(c.p.pose, 'stand');
	const t = c.t * c.speed;
	const w = c.idle ? Math.sin(t * 9) : 0;
	const sw = 12;
	let la: [number, number];
	let ra: [number, number];
	switch (pose) {
		case 'wave':
			la = [200, 20];
			ra = [-60 + w * 22, -60 + w * 22];
			break;
		case 'panic':
			la = [-130 + w * 15, -130 + w * 15];
			ra = [-50 - w * 15, -50 - w * 15];
			break;
		case 'point':
			la = [110, 80];
			ra = [-8, -8];
			break;
		case 'shrug':
			la = [160, -110];
			ra = [20, -70];
			break;
		default:
			la = [112, 98];
			ra = [68, 82];
	}
	const sh: Pt = [100, 128];
	const breathe = c.idle ? Math.sin(t * 2) * 1.5 : 0;
	const legs = pose === 'run' ? Math.sin(t * 10) * 26 : 0;
	// filled flat-shaded silhouette (orca review: the line-stroke stick figure read as placeholder art next to the
	// vector animals): thick capsule limbs + a torso, white fill with a ~6 px navy outline; style "stick" = old look
	const stick = str(c.p.style, 'filled') === 'stick';
	const line = paint(c, str(c.p.outline, dv ? '#c9d6dc' : '#0b1a22'));
	const limbW = stick ? sw : 26;
	const ol = stick ? 0 : dv ? 7 : 12; // outline drawn as a wider navy pass under the white (diver: thin light rim)
	const armD = (a: [number, number]) => {
		const e = polar(sh, a[0], 52);
		const h = polar(e, a[1], 50);
		return `M ${sh[0]} ${sh[1]} L ${e[0]} ${e[1]} L ${h[0]} ${h[1]}`;
	};
	const legL = `M 88 206 L ${72 - legs} 274 L ${68 - legs} 336`;
	const legR = `M 112 206 L ${128 + legs} 274 L ${132 + legs} 336`;
	const torso = `M 76 ${100 + breathe} C 76 ${90 + breathe} 124 ${90 + breathe} 124 ${100 + breathe} L 120 214 C 112 222 88 222 80 214 Z`;
	const pass = (stroke: string, extra: number, key: string) => (
		<g key={key}>
			{[armD(la), armD(ra), legL, legR].map((d, i) => (
				<path key={i} d={d} stroke={stroke} strokeWidth={limbW + extra} strokeLinecap="round" strokeLinejoin="round" fill="none" />
			))}
			{stick ? (
				<path d={`M 100 ${86 + breathe} L 100 212`} stroke={stroke} strokeWidth={sw + 2} strokeLinecap="round" />
			) : (
				<path d={torso} fill={stroke} stroke={stroke} strokeWidth={extra} strokeLinejoin="round" />
			)}
			<circle cx={100} cy={52 + breathe} r={34 + extra / 2} fill={stroke} />
		</g>
	);
	const fins = [
		[68 - legs, -1],
		[132 + legs, 1],
	].map(([x, s], i) => (
		<path key={`fin${i}`} d={`M ${x - 14} 330 L ${x + s * 4 - 18} 360 L ${x + s * 4 + 18} 360 L ${x + 14} 330 Z`} fill={paint(c, '#f5c02e')} stroke={paint(c, '#c9961c')} strokeWidth={3} strokeLinejoin="round" />
	));
	if (dv)
		return (
			<g>
				<rect x={114} y={84} width={30} height={96} rx={13} fill={paint(c, '#d8d8d8')} stroke={line} strokeWidth={4} />
				{pass(line, ol, 'o')}
				{pass(col, 0, 'f')}
				{fins}
				<rect x={74} y={34 + breathe} width={52} height={24} rx={10} fill={paint(c, '#0a0c0e')} />
				{c.sil ? null : <rect x={79} y={38 + breathe} width={42} height={16} rx={6} fill="#6fd6e8" />}
				{c.sil ? null : <path d={`M 84 ${150 + breathe} L 116 ${150 + breathe}`} stroke="#2b3138" strokeWidth={5} strokeLinecap="round" />}
			</g>
		);
	return (
		<g>
			{ol ? pass(line, ol, 'o') : null}
			{pass(col, 0, 'f')}
			{stick ? null : <path d={`M 84 ${150 + breathe} L 116 ${150 + breathe}`} stroke={paint(c, '#c9d3d8')} strokeWidth={5} strokeLinecap="round" opacity={0.7} />}
		</g>
	);
};

const you: Figure = {label: 'YOU', box: [24, 12, 152, 344], size: 1.75, axis: 'h', draw: youDraw};

// ================================================================ city bus

const bus: Figure = {
	label: 'CITY BUS',
	box: [0, 20, 1200, 312],
	size: 12,
	axis: 'w',
	draw: (c) => {
		const spin = c.idle ? c.t * 0 : 0;
		const wheel = (x: number) => (
			<g key={x} transform={`rotate(${spin} ${x} 282)`}>
				<circle cx={x} cy={282} r={50} fill={paint(c, '#15191d')} />
				{c.sil ? null : <circle cx={x} cy={282} r={24} fill="#9aa3a9" />}
				{c.sil ? null : <circle cx={x} cy={282} r={8} fill="#4b545a" />}
			</g>
		);
		return (
			<g>
				<rect x={0} y={20} width={1200} height={250} rx={30} fill={paint(c, '#f2b632')} />
				{c.sil ? null : (
					<g>
						<rect x={0} y={196} width={1200} height={30} fill="#d9961c" />
						<rect x={0} y={20} width={1200} height={22} rx={11} fill="#f7c95a" />
						{Array.from({length: 9}, (_, i) => (
							<rect key={i} x={70 + i * 108} y={60} width={92} height={92} rx={10} fill="#1d2a33" />
						))}
						{Array.from({length: 9}, (_, i) => (
							<path key={`g${i}`} d={`M ${82 + i * 108} 70 L ${110 + i * 108} 70 L ${86 + i * 108} 120 Z`} fill="#ffffff" opacity={0.12} />
						))}
						<rect x={1060} y={60} width={110} height={190} rx={12} fill="#1d2a33" />
						<rect x={1150} y={60} width={40} height={120} rx={12} fill="#2b3c48" />
						<rect x={1176} y={208} width={20} height={26} rx={6} fill="#fff6c9" />
						<rect x={4} y={208} width={14} height={26} rx={5} fill="#d6453a" />
						<text x={600} y={186} textAnchor="middle" fontFamily='"Montserrat", sans-serif' fontWeight={900} fontSize={30} letterSpacing={4} fill="#1d2a33">
							{str(c.p.text, 'CITY BUS')}
						</text>
					</g>
				)}
				{wheel(230)}
				{wheel(950)}
			</g>
		);
	},
};

// ================================================================ car

const car: Figure = {
	label: 'CAR',
	box: [0, 30, 450, 140],
	size: 4.5,
	axis: 'w',
	draw: (c) => {
		const col = str(c.p.color, '#3f8fd2');
		return (
			<g>
				<path d="M 10 120 C 10 96 30 88 60 84 L 120 80 C 150 46 190 32 250 32 C 300 32 330 50 360 80 L 410 88 C 436 92 446 104 444 124 C 444 140 432 146 420 146 L 20 146 C 12 146 10 136 10 120 Z" fill={paint(c, col)} />
				{c.sil ? null : (
					<g>
						<path d="M 140 80 C 165 54 196 44 236 44 L 236 80 Z" fill="#1d2a33" />
						<path d="M 252 44 C 292 44 318 56 340 80 L 252 80 Z" fill="#1d2a33" />
						<rect x={420} y={100} width={18} height={12} rx={4} fill="#fff6c9" />
					</g>
				)}
				{[100, 350].map((x) => (
					<g key={x}>
						<circle cx={x} cy={146} r={30} fill={paint(c, '#15191d')} />
						{c.sil ? null : <circle cx={x} cy={146} r={13} fill="#9aa3a9" />}
					</g>
				))}
			</g>
		);
	},
};

// ================================================================ elephant

const elephant: Figure = {
	label: 'ELEPHANT',
	box: [40, 58, 560, 362],
	size: 3.3,
	axis: 'h',
	draw: (c) => {
		const t = c.t * c.speed;
		const trunk = c.idle ? Math.sin(t * 1.4) * 6 : 0;
		const ear = c.idle ? Math.sin(t * 1.9) * 4 : 0;
		const g = paint(c, '#8b9096');
		const dk = paint(c, '#6f747a');
		return (
			<g>
				<rect x={150} y={250} width={64} height={168} rx={18} fill={dk} />
				<rect x={380} y={250} width={64} height={168} rx={18} fill={dk} />
				<path d="M 60 220 C 60 120 150 80 290 80 C 380 80 440 100 470 140 C 500 180 500 260 470 290 C 420 320 300 320 200 316 C 110 312 60 290 60 220 Z" fill={g} />
				<path d="M 60 200 C 46 214 40 240 44 270" stroke={g} strokeWidth={8} strokeLinecap="round" fill="none" />
				<rect x={110} y={260} width={66} height={160} rx={18} fill={g} />
				<rect x={340} y={260} width={66} height={160} rx={18} fill={g} />
				<g transform={`rotate(${trunk} 540 200)`}>
					<path d="M 520 150 C 560 180 570 260 556 330 C 552 350 560 372 580 380 C 590 386 584 400 570 398 C 540 392 524 360 528 330 C 536 270 520 220 500 200 Z" fill={g} />
				</g>
				<path d="M 430 80 C 480 50 540 70 560 120 C 576 160 566 200 540 220 C 520 236 490 230 470 220 Z" fill={g} />
				<g transform={`rotate(${ear} 450 120)`}>
					<path d="M 440 90 C 400 80 370 110 372 160 C 374 210 400 250 440 250 C 470 250 480 200 470 150 C 466 120 456 100 440 90 Z" fill={dk} />
				</g>
				{c.sil ? null : <path d="M 540 230 C 560 240 580 240 600 230 C 590 246 566 252 544 246 Z" fill="#efe8d8" />}
				{c.sil ? null : <circle cx={510} cy={130} r={6} fill="#141618" />}
			</g>
		);
	},
};

export const PEOPLE: Record<string, Figure> = {diver, you, bus, car, elephant};
