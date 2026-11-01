import React from 'react';
import {E, blinking, camAt, camT, clamp, look, para, talkMouth} from '../lib/anim';
import {LOOKS, Soldier} from '../art/soldier';
import {CloudBand, Crate, PoleFlag, Quonset, Sparkle, Streaks, streakSet} from '../art/props';

// Scene block 9 (49.70-56.00): Ukrainian camp. S24 wide, S25 push + rotate to G, S26 CU with sparkles (end).

const CLOUDS: [number, number, number][] = [
	[120, 140, 1.0],
	[520, 80, 0.8],
	[820, 230, 1.0],
	[1100, 120, 0.9],
	[300, 330, 0.7],
	[1400, 300, 0.8],
	[-100, 420, 0.7],
];
const GRASS = streakSet(52, 18, -500, 1700, 900, 2000, 140, 420, 26);

const GX = 640;
const GY = 1180;
const GS = 0.62;

export const Camp: React.FC<{t: number}> = ({t}) => {
	const pop = E.outBack(clamp((t - 51.5) / 0.5));
	const gFace: [number, number] = [GX + 10 * GS, GY - 537 * GS - 120 * (1 - 1) ];
	const c = camAt(t, [
		[49.7, {x: 540, y: 960, s: 1, r: 0}],
		[52.4, {x: 545, y: 958, s: 1.05, r: 0}, E.linear],
		[53.8, look(gFace, [600, 640], 3.0, -15), E.inOutCubic],
		[54.0, look(gFace, [600, 640], 3.02, -15), E.linear],
		[56.1, look([gFace[0] - 6, gFace[1] - 6], [640, 620], 3.2, -16), E.linear],
	]);
	const cFront = para(c, 1.3, 545, 958);
	const lift = E.outCubic(clamp((t - 54.1) / 0.6));
	const gy = GY + (1 - pop) * 220;
	return (
		<g>
			<g transform={camT(c)}>
				<rect x={-800} y={-800} width={2700} height={1800} fill="#AEDDFA" />
				<rect x={-800} y={500} width={2700} height={400} fill="#DCEFFD" opacity={0.6} />
				<CloudBand t={t} items={CLOUDS} w={1900} x0={-400} />
				{/* hills + tent */}
				<path d="M-800,880 Q-300,620 200,760 Q600,560 1100,700 Q1500,600 1900,760 L1900,1000 L-800,1000 Z" fill="#6E9649" />
				<path d="M560,880 L700,520 Q860,470 1060,520 L1240,880 Z" fill="#4A6833" />
				<path d="M880,880 L960,560 L1000,880 Z" fill="#3B5528" />
				<path d="M700,520 Q860,470 1060,520 L1050,540 Q860,495 712,540 Z" fill="#5E7E44" />
				{/* flags + watchtower */}
				<PoleFlag x={135} y={500} h={300} fw={330} kind="ua" t={t} />
				<PoleFlag x={772} y={540} h={220} fw={200} kind="ua" t={t} seed={2.2} />
				<g transform="translate(20 495)">
					<rect x={-70} y={-200} width={150} height={24} fill="#526F39" />
					<rect x={-60} y={-176} width={130} height={60} fill="#648A42" />
					<path d="M-50,-116 L-70,200 M60,-116 L80,200 M-60,-40 L70,-40 M-60,60 L70,60" stroke="#526F39" strokeWidth={14} />
					<path d="M-80,-200 L5,-250 L90,-200 Z" fill="#526F39" />
				</g>
				{/* green quonset */}
				<Quonset x={300} y={975} w={720} h={480} c="#648A42" rim="#7FA55A" dark="#3B5528" door="#2E3A5A" strut="#526F39" doorW={160} doorHi="#5E6E92" />
				<rect x={-800} y={860} width={2700} height={1500} fill="#7A8F28" />
				<Streaks items={GRASS} c="#879C33" />
				<rect x={-800} y={860} width={2700} height={14} fill="#6E8424" />
				{/* G, who pops up from behind the crates */}
				<Soldier
					look={LOOKS.G}
					x={GX}
					y={gy}
					s={GS}
					pose={{
						facing: -1,
						gun: {kind: 'm4', x: 40 - lift * 10, y: -380 - lift * 30 + Math.sin(t * 2) * 4, rot: -60 - lift * 10},
						handN: 'grip',
						handF: 'fore',
						mouth: t > 51.6 ? (t > 54 ? (t % 0.8 < 0.5 ? 'grin' : 'smile') : talkMouth(t, 11, 'grin')) : 'closed',
						brows: t > 54 ? 'happy' : 'neutral',
						eyes: blinking(t, 71) ? 'closed' : 'open',
						headRot: Math.sin(t * 3) * 3,
						headY: Math.sin(t * 6) * 2,
						lookX: 2,
						breathe: t * 0.4,
					}}
				/>
			</g>
			{/* foreground crates with parallax */}
			<g transform={camT(cFront)}>
				<Crate x={20} y={910} w={380} h={230} />
				<Crate x={760} y={900} w={280} h={240} c="#727748" />
				<Crate x={-60} y={1080} w={420} h={300} c="#666B3E" />
				<Crate x={340} y={1060} w={360} h={250} />
				<Crate x={700} y={1100} w={420} h={300} c="#666B3E" />
			</g>
			<Sparkle t={t} t0={54.4} x={330} y={290} size={500} />
			<Sparkle t={t} t0={54.75} x={560} y={700} size={260} spin={-30} />
			<Sparkle t={t} t0={55.1} x={380} y={520} size={340} />
			<Sparkle t={t} t0={55.3} x={600} y={820} size={80} />
		</g>
	);
};
