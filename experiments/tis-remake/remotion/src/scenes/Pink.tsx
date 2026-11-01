import React from 'react';
import {E, FPS, blinking, camAt, camT, clamp, hash, kf, lerp, para, rng} from '../lib/anim';
import {Gun, GunPose} from '../art/guns';
import {Head, LOOKS, Soldier} from '../art/soldier';
import {CloudBand, Explosion, Hedgehog, MuzzleFlash, Streaks, Wire, streakSet} from '../art/props';
import {P} from '../art/defs';

// Scene block 6 (32.43-38.93): pink sunset ruins. S17 F yelling, S18 truck + explosion cover, S19 barricade.

const CLOUDS: [number, number, number][] = [
	[60, 120, 1.0],
	[460, 60, 0.9],
	[820, 200, 1.1],
	[1250, 90, 1.0],
	[1650, 180, 0.9],
];

const Block: React.FC<{x: number; y: number; w: number; h: number; c: string; side: string; win: string; seed: number; cols?: number; rows?: number; blown?: number}> = ({x, y, w, h, c, side, win, seed, cols = 3, rows = 8, blown = 0.3}) => {
	const R = rng(seed);
	const ww = (w - 40) / cols - 30;
	const wins = [];
	for (let r = 0; r < rows; r++)
		for (let k = 0; k < cols; k++) {
			const wx = x + 30 + k * ((w - 40) / cols);
			const wy = y + 40 + r * 130;
			if (wy + 90 > y + h) continue;
			const b = R() < blown;
			wins.push(
				<g key={`${r}_${k}`}>
					<rect x={wx} y={wy} width={ww} height={86} fill={b ? '#451233' : win} />
					{!b && <rect x={wx} y={wy + 70} width={ww} height={16} fill="#000" opacity={0.15} />}
					{b && <path d={`M${wx - 8},${wy + 30} L${wx + 10},${wy - 10} L${wx + ww * 0.6},${wy - 14} L${wx + ww + 12},${wy + 20} L${wx + ww + 6},${wy + 96} L${wx - 10},${wy + 92} Z`} fill="#451233" />}
					<rect x={wx - 6} y={wy + 86} width={ww + 12} height={10} rx={3} fill={side} opacity={0.7} />
				</g>,
			);
		}
	return (
		<g>
			<rect x={x} y={y} width={w} height={h} fill={c} />
			<rect x={x + w - 34} y={y} width={34} height={h} fill={side} />
			<rect x={x} y={y} width={w} height={14} fill="#FFFFFF" opacity={0.18} />
			{wins}
			<path d={`M${x + w * 0.3},${y + 80} L${x + w * 0.38},${y + 200} L${x + w * 0.3},${y + 320} L${x + w * 0.42},${y + 420}`} stroke={side} strokeWidth={5} fill="none" strokeLinecap="round" />
		</g>
	);
};

const SmallShooter: React.FC<{x: number; y: number; t: number; seed: number; look: keyof typeof LOOKS}> = ({x, y, t, seed, look}) => {
	const f = Math.floor(t * FPS);
	const g: GunPose = {kind: 'ak47', x: 120, y: -400 - (f % 3 === 0 ? 0 : 3), rot: -4};
	return (
		<g>
			<Soldier look={LOOKS[look]} x={x} y={y} s={0.34} shadow={false} pose={{facing: 1, gun: g, handN: 'grip', handF: 'fore', mouth: 'flat', brows: 'angry', lean: 6, headX: 12}} />
			<g transform={`translate(${x + 0.34 * 330} ${y - 0.34 * 405})`}>
				<MuzzleFlash frame={f} size={46} seed={seed} />
			</g>
		</g>
	);
};

const FrontLine: React.FC<{t: number}> = ({t}) => (
	<g>
		<rect x={-1000} y={-800} width={4000} height={1900} fill="#94A2EB" />
		<CloudBand t={t} items={CLOUDS} w={2000} x0={-200} c="#DECECE" sh="#94A1F1" />
		<Block x={-60} y={430} w={360} h={700} c="#F6C2B1" side="#DD7480" win="#602A3A" seed={2} />
		<Block x={420} y={560} w={420} h={600} c="#EFAA9B" side="#C36170" win="#602A3A" seed={3} />
		{/* collapsed red block */}
		<path d="M780,1000 L780,620 L860,560 L960,640 L1030,600 L1100,700 L1120,1000 Z" fill="#C4675E" />
		<path d="M820,700 L880,690 L880,780 L820,790 Z M960,720 L1020,716 L1020,800 L960,806 Z" fill="#451233" />
		<path d="M780,620 L860,560 L870,580 L790,640 Z" fill="#E08A80" />
		<Block x={940} y={-200} w={420} h={1300} c="#FCD5B1" side="#DD7480" win="#451233" seed={7} cols={2} rows={10} blown={0.4} />
		<Block x={1460} y={200} w={500} h={900} c="#F6C2B1" side="#C36170" win="#602A3A" seed={9} />
		{/* ground + rubble barricade */}
		<rect x={-1000} y={960} width={4000} height={1500} fill="#ECB8A9" />
		<Streaks items={streakSet(21, 18, -800, 2600, 1000, 1200, 120, 380, 22)} c="#D89998" />
		<rect x={-1000} y={1180} width={4000} height={1500} fill="#7A4F49" />
		<SmallShooter x={660} y={1010} t={t} seed={2} look="F" />
		<SmallShooter x={760} y={1030} t={t + 0.1} seed={5} look="H" />
		<Wreck x={500} y={1062} />
	</g>
);

/** Rubble barricade with a burnt-out car, slabs, rebar and coiled wire (S17 background). */
const Wreck: React.FC<{x: number; y: number}> = ({x, y}) => {
	const R = rng(77);
	const bars = Array.from({length: 9}, (_, i) => {
		const bx = 20 + R() * 500;
		const a = -150 + R() * 120;
		const L = 50 + R() * 70;
		const by = -40 - R() * 50;
		return [bx, by, bx + Math.cos((a * Math.PI) / 180) * L, by + Math.sin((a * Math.PI) / 180) * L, i] as const;
	});
	return (
		<g transform={`translate(${x} ${y})`}>
			{/* rubble heap */}
			<path d="M0,0 Q30,-70 110,-80 Q170,-120 260,-96 Q330,-130 420,-92 Q490,-84 540,0 Z" fill="#6E4440" />
			<path d="M0,0 Q30,-70 110,-80 Q90,-50 80,0 Z" fill="#5A3532" />
			{/* burnt-out car: crumpled body, empty windows, wheel arches */}
			<g transform="translate(150 -92) rotate(-6)">
				<path d="M0,40 L8,0 L60,-6 L96,-46 L210,-48 L246,-8 L300,0 L306,40 Z" fill="#4A2525" />
				<path d="M100,-40 L150,-42 L150,-10 L80,-8 Z M160,-42 L206,-42 L232,-10 L160,-10 Z" fill="#2A1513" />
				<path d="M8,0 L60,-6 L96,-46 L210,-48 L214,-42 L100,-40 L64,0 Z" fill="#7A3E38" opacity={0.7} />
				<circle cx={64} cy={42} r={28} fill="#1E1110" />
				<circle cx={64} cy={42} r={12} fill="#3A2522" />
				<circle cx={246} cy={42} r={28} fill="#1E1110" />
				<circle cx={246} cy={42} r={12} fill="#3A2522" />
				<path d="M120,-20 L132,6 M180,-26 L172,4" stroke="#1E1110" strokeWidth={4} strokeLinecap="round" />
			</g>
			{/* broken slabs */}
			<path d="M330,-60 L420,-110 L450,-80 L360,-30 Z" fill="#9A6A62" />
			<path d="M330,-60 L420,-110 L424,-102 L336,-54 Z" fill="#C0897E" />
			<path d="M30,-40 L120,-70 L130,-46 L40,-20 Z" fill="#8A5C55" />
			{/* rebar sticking out */}
			{bars.map(([x1, y1, x2, y2, i]) => (
				<g key={i}>
					<line x1={x1} y1={y1} x2={x2} y2={y2} stroke="#2A1B17" strokeWidth={6} strokeLinecap="round" />
					<line x1={x1} y1={y1 - 2} x2={x2} y2={y2 - 2} stroke="#7A4F49" strokeWidth={2} strokeLinecap="round" />
				</g>
			))}
			{/* coiled wire along the top */}
			{Array.from({length: 14}, (_, i) => (
				<ellipse key={i} cx={20 + i * 36} cy={-96 + Math.sin(i * 1.3) * 10} rx={22} ry={16} fill="none" stroke="#2A1B17" strokeWidth={3} />
			))}
			{/* debris chunks at the foot */}
			{[30, 120, 210, 300, 400, 480].map((dx, i) => (
				<rect key={dx} x={dx} y={-14 - (i % 2) * 6} width={26 + (i % 3) * 8} height={14} rx={3} fill={i % 2 ? '#5A3532' : '#8A5C55'} transform={`rotate(${(i % 3) * 12 - 10} ${dx} 0)`} />
			))}
		</g>
	);
};

/** Prone soldier drawn lying left (head on the left), elbow-crawling. */
const Prone: React.FC<{t: number; x: number; y: number}> = ({t, x, y}) => {
	const ph = t * 1.2;
	const slide = Math.sin(ph * Math.PI) * 15;
	const l1 = Math.sin(ph * Math.PI * 2) * 20;
	const f = Math.floor(t * FPS);
	const g: GunPose = {kind: 'ak12', x: -230, y: -60, rot: 180};
	return (
		<g transform={`translate(${x + slide} ${y})`}>
			<ellipse cx={0} cy={20} rx={290} ry={22} fill="url(#softShadow)" />
			{/* legs */}
			<path d={`M60,-44 L180,${-34 + l1} L262,${-38 + l1}`} fill="none" stroke="url(#camoRU)" strokeWidth={72} strokeLinecap="round" strokeLinejoin="round" />
			<path d={`M60,-30 L180,${-10 - l1} L262,${-6 - l1}`} fill="none" stroke="url(#camoRU)" strokeWidth={72} strokeLinecap="round" strokeLinejoin="round" />
			<path d={`M60,-30 L180,${-10 - l1} L262,${-6 - l1}`} fill="none" stroke="#000" strokeOpacity={0.12} strokeWidth={72} strokeLinecap="round" />
			<g transform={`translate(292 ${-34 + l1}) rotate(-90)`}>
				<rect x={-30} y={-20} width={60} height={70} rx={14} fill={P.boot} />
			</g>
			<g transform={`translate(292 ${-2 - l1}) rotate(-90)`}>
				<rect x={-30} y={-20} width={60} height={70} rx={14} fill={P.boot} />
				<rect x={-30} y={40} width={60} height={12} rx={5} fill="#0E0D0B" />
			</g>
			{/* torso lying */}
			<rect x={-160} y={-124} width={240} height={124} rx={50} fill="url(#camoRU)" />
			<rect x={-140} y={-112} width={190} height={84} rx={16} fill="url(#camoRUdk)" />
			{[-120, -70, -20].map((px) => (
				<rect key={px} x={px} y={-106} width={40} height={30} rx={8} fill="#3A3926" />
			))}
			{/* head looking forward-left */}
			<g transform="translate(-190 -66) rotate(-8) scale(-1 1) scale(0.95)">
				<Head look={LOOKS.D} pose={{mouth: 'flat', brows: 'angry', eyes: blinking(t, 41) ? 'closed' : 'open', lookX: 2}} />
			</g>
			{/* arms + gun */}
			<path d={`M-120,-60 L-200,${-8 + Math.sin(ph * Math.PI * 2) * 6} L-260,-50`} fill="none" stroke="url(#camoRU)" strokeWidth={50} strokeLinecap="round" strokeLinejoin="round" />
			<Gun g={g} />
			<circle cx={-200} cy={-40} r={33} fill={P.hand} />
			<circle cx={-322} cy={-62} r={33} fill={P.hand} />
			<g transform={`translate(${-230 - 200} -62)`}>{f % 24 < 14 && <MuzzleFlash frame={f} size={90} seed={9} />}</g>
		</g>
	);
};

const Barricade: React.FC<{t: number}> = ({t}) => {
	const f = Math.floor(t * FPS);
	const standG: GunPose = {kind: 'ak12', x: 150 - (f % 3 === 0 ? 8 : 0), y: -440, rot: -2};
	const sparks = [0, 1, 2, 3].map((i) => {
		const per = 0.9 + hash(i) * 0.6;
		const ph = ((t + hash(i + 4) * per) % per) / per;
		return {x: [120, 900, 160, 960][i] + hash(i + 9) * 40, y: [820, 860, 960, 930][i], k: ph < 0.15 ? Math.sin((ph / 0.15) * Math.PI) : 0};
	});
	return (
		<g>
			<rect x={-600} y={-400} width={2600} height={1500} fill="#F6C2B1" />
			<Block x={-80} y={-260} w={420} h={1300} c="#FCD5B1" side="#DD7480" win="#602A3A" seed={11} cols={2} rows={10} />
			<Block x={380} y={-300} w={460} h={1340} c="#EFAA9B" side="#C36170" win="#451233" seed={12} cols={2} rows={10} blown={0.6} />
			<Block x={880} y={-240} w={520} h={1280} c="#F6C2B1" side="#DD7480" win="#602A3A" seed={13} cols={3} rows={10} blown={0.45} />
			<path d="M180,380 L260,450 L250,560 L330,640 M560,120 L640,180 L700,170 L760,240" stroke="#B05060" strokeWidth={6} fill="none" strokeLinecap="round" />
			<rect x={-600} y={990} width={2600} height={70} fill="#ECB8A9" />
			<rect x={-600} y={1050} width={2600} height={1600} fill="#7A4F49" />
			<Streaks items={streakSet(31, 16, -500, 1800, 1100, 1900, 140, 420, 26)} c="#86594F" />
			{/* standing shooter behind the wire */}
			<Soldier look={LOOKS.H} x={690} y={980} s={0.7} pose={{facing: -1, gun: standG, handN: 'grip', handF: 'fore', brows: 'angry', mouth: 'flat', lean: 5, headX: 10, eyes: blinking(t, 44) ? 'closed' : 'open', lookX: 2}} />
			<g transform={`translate(${690 - 0.7 * (standG.x + 222) - 30} ${980 - 0.7 * 445})`}>
				<MuzzleFlash frame={f} size={95} seed={3} />
			</g>
			<Hedgehog x={230} y={890} />
			<Hedgehog x={850} y={890} />
			{[800, 845, 895, 945, 995].map((y, i) => (
				<Wire key={y} x0={-300} x1={1500} y={y} sag={6 + i} seed={i * 13} />
			))}
			{sparks.map((s, i) => (s.k > 0 ? <path key={i} transform={`translate(${s.x} ${s.y}) scale(${s.k * 26})`} d="M0,-1 L0.25,-0.25 L1,0 L0.25,0.25 L0,1 L-0.25,0.25 L-1,0 L-0.25,-0.25 Z" fill="#FFD34D" /> : null))}
			<Prone t={t} x={650} y={1150} />
		</g>
	);
};

export const Pink: React.FC<{t: number}> = ({t}) => {
	if (t < 35.1) {
		// S17 holds on F, then a fast whip right (F is out of frame by 34.75) under the explosion cover
		const c = camAt(t, [
			[32.43, {x: 540, y: 960, s: 1, r: 0}],
			[34.38, {x: 545, y: 955, s: 1.05, r: 0}, E.linear],
			[34.78, {x: 545 + 700, y: 955, s: 1.05, r: 0}, E.inOutCubic],
			[35.1, {x: 545 + 820, y: 955, s: 1.05, r: 0}, E.outCubic],
		]);
		const cF = para(c, 1.5, 545, 955);
		const yell = t > 32.5;
		const ex = clamp((t - EX0) / EXD);
		return (
			<g>
				<g transform={camT(c)}>
					<FrontLine t={t} />
				</g>
				<g transform={camT(cF)}>
					{/* S17: F as a huge left-half close-up (head ~600 px tall), the AK-47 across the bottom */}
					<Soldier
						look={LOOKS.F}
						x={128}
						y={2330}
						s={3.3}
						pose={{
							facing: 1,
							gun: {kind: 'ak47', x: 90, y: -262, rot: -6, lod: 2},
							handN: 'grip',
							handF: 'fore',
							mouth: yell ? (t % 0.5 < 0.36 ? 'yell' : 'open') : 'flat',
							brows: 'angry',
							eyes: blinking(t, 51) ? 'closed' : 'open',
							headX: yell ? 4 + Math.sin(t * 6) * 3 : 0,
							headRot: Math.sin(t * 2.2) * 3,
							lean: 2,
							breathe: t * 0.6,
							lookX: 2,
						}}
					/>
				</g>
				{ex > 0 && ex < 1 && <ExplosionCover u={ex} />}
			</g>
		);
	}
	const c = camAt(t, [
		[35.1, {x: 540, y: 960, s: 1.06, r: 0}],
		[35.25, {x: 545, y: 960, s: 1.06, r: 0}, E.linear],
		[38.95, {x: 745, y: 960, s: 1.06, r: 0}, E.linear],
	]);
	const ex = clamp((t - EX0) / EXD);
	return (
		<g>
			<g transform={camT(c)}>
				<Barricade t={t} />
			</g>
			{ex > 0 && ex < 1 && <ExplosionCover u={ex} />}
		</g>
	);
};

// Explosion cover: enters from the lower right at 34.55, fills the whole frame from ~34.78 to ~35.12
// (the S18->S19 cut at 35.10 happens under it), then shrinks away to the lower left.
const EX0 = 34.55;
const EXD = 0.8;
const ExplosionCover: React.FC<{u: number}> = ({u}) => {
	const x = kf(u, [
		[0, 1150],
		[0.3, 560, E.outCubic],
		[0.7, 520],
		[1, -300, E.inCubic],
	]);
	const y = kf(u, [
		[0, 1700],
		[0.3, 960, E.outCubic],
		[0.7, 980],
		[1, 1800, E.inCubic],
	]);
	const s = kf(u, [
		[0, 260],
		[0.3, 3500, E.outCubic],
		[0.7, 3700],
		[1, 400, E.inCubic],
	]);
	const core = kf(u, [
		[0, 0],
		[0.25, 1],
		[0.72, 1],
		[0.85, 0],
	]);
	return (
		<g transform={`translate(${x} ${y})`}>
			<Explosion size={s} rot={lerp(-40, 80, u)} core={core} />
		</g>
	);
};
