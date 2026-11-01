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
		<path d="M560,1060 Q600,960 700,990 Q780,940 860,990 Q950,960 1010,1060 Z" fill="#7A504A" />
		<path d="M600,1060 L640,1000 L700,1030 L760,990 L800,1040 Z" fill="#2A1B17" />
		<path d="M880,980 L960,930 M900,1000 L1000,960" stroke="#2A1B17" strokeWidth={10} strokeLinecap="round" />
	</g>
);

/** Prone soldier drawn lying left (head on the left), elbow-crawling. */
const Prone: React.FC<{t: number; x: number; y: number}> = ({t, x, y}) => {
	const ph = t * 1.2;
	const slide = Math.sin(ph * Math.PI) * 15;
	const l1 = Math.sin(ph * Math.PI * 2) * 20;
	const f = Math.floor(t * FPS);
	const g: GunPose = {kind: 'ak12', x: -230, y: -60, rot: 180};
	return (
		<g transform={`translate(${x + slide} ${y})`}>
			<ellipse cx={20} cy={20} rx={330} ry={22} fill="url(#softShadow)" />
			{/* legs */}
			<path d={`M60,-40 L220,${-30 + l1} L330,${-34 + l1}`} fill="none" stroke="url(#camoRU)" strokeWidth={62} strokeLinecap="round" strokeLinejoin="round" />
			<path d={`M60,-30 L220,${-10 - l1} L330,${-6 - l1}`} fill="none" stroke="url(#camoRU)" strokeWidth={62} strokeLinecap="round" strokeLinejoin="round" />
			<path d={`M60,-30 L220,${-10 - l1} L330,${-6 - l1}`} fill="none" stroke="#000" strokeOpacity={0.12} strokeWidth={62} strokeLinecap="round" />
			<g transform={`translate(360 ${-30 + l1}) rotate(-90)`}>
				<rect x={-30} y={-20} width={60} height={70} rx={14} fill={P.boot} />
			</g>
			<g transform={`translate(360 ${-2 - l1}) rotate(-90)`}>
				<rect x={-30} y={-20} width={60} height={70} rx={14} fill={P.boot} />
				<rect x={-30} y={40} width={60} height={12} rx={5} fill="#0E0D0B" />
			</g>
			{/* torso lying */}
			<rect x={-160} y={-110} width={250} height={110} rx={46} fill="url(#camoRU)" />
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
			<g transform={`translate(${-230 - 200} -62)`}>{f % 50 < 12 && <MuzzleFlash frame={f} size={70} seed={9} />}</g>
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
			<Soldier look={LOOKS.H} x={690} y={980} s={0.62} pose={{facing: -1, gun: standG, handN: 'grip', handF: 'fore', brows: 'angry', mouth: 'flat', lean: 5, headX: 10, eyes: blinking(t, 44) ? 'closed' : 'open', lookX: 2}} />
			<g transform={`translate(${690 - 0.62 * (standG.x + 214) - 26} ${980 - 0.62 * 445})`}>
				<MuzzleFlash frame={f} size={70} seed={3} />
			</g>
			<Hedgehog x={130} y={890} />
			<Hedgehog x={920} y={890} />
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
		const c = camAt(t, [
			[32.43, {x: 540, y: 960, s: 1, r: 0}],
			[34.5, {x: 545, y: 955, s: 1.05, r: 0}, E.linear],
			[35.1, {x: 545 + 900, y: 955, s: 1.05, r: 0}, E.inCubic],
		]);
		const cF = para(c, 1.5, 545, 955);
		const yell = t > 32.5;
		const ex = clamp((t - 34.9) / 0.37);
		return (
			<g>
				<g transform={camT(c)}>
					<FrontLine t={t} />
				</g>
				<g transform={camT(cF)}>
					<Soldier
						look={LOOKS.F}
						x={321}
						y={1965}
						s={2.43}
						pose={{
							facing: 1,
							gun: {kind: 'ak47', x: 70, y: -270, rot: -4},
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
	const ex = clamp((t - 34.9) / 0.37);
	return (
		<g>
			<g transform={camT(c)}>
				<Barricade t={t} />
			</g>
			{ex > 0 && ex < 1 && <ExplosionCover u={ex} />}
		</g>
	);
};

const ExplosionCover: React.FC<{u: number}> = ({u}) => {
	const x = kf(u, [
		[0, 1250],
		[0.5, 560, E.outCubic],
		[1, -250, E.inCubic],
	]);
	const y = kf(u, [
		[0, 1750],
		[0.5, 980, E.outCubic],
		[1, 1750, E.inCubic],
	]);
	const s = kf(u, [
		[0, 300],
		[0.5, 950],
		[1, 500],
	]);
	return (
		<g transform={`translate(${x} ${y})`}>
			<Explosion size={s} rot={lerp(-40, 80, u)} />
		</g>
	);
};
