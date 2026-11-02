/**
 * stick/Set: flat style A backgrounds for the story lane (1080 x 1920 frame, sliced to the box).
 * Big simple shapes, one flat shadow per object, far layers paler; floors put feet at y ~1150-1300.
 *
 * props
 *   place   hall | hallNight | salon | facade | museum | blueprint
 *   fire    0..1 track (museum): flames out of the windows and roof, smoke
 *   seed
 */
import React from 'react';
import type {KitComponentProps} from '../../../core/registry';
import {clamp, str, track} from '../util';
import {c, f, hash} from './common';

const W = 1080;
const H = 1920;

function Chandelier({x, y, t, lit}: {x: number; y: number; t: number; lit: boolean}) {
	const sway = Math.sin(t * 0.9) * 1.5;
	return (
		<g transform={`rotate(${f(sway)} ${x} 0)`}>
			<rect x={x - 4} y={0} width={8} height={y - 60} fill={c('amber-2')} />
			{lit && <circle cx={x} cy={y} r={170} fill={c('amber-4')} opacity={0.16} />}
			<ellipse cx={x} cy={y} rx={150} ry={26} fill={c('amber-3')} />
			<ellipse cx={x} cy={y + 8} rx={150} ry={18} fill={c('amber-1')} />
			<path d={`M ${x - 40} ${y - 60} L ${x + 40} ${y - 60} L ${x + 18} ${y} L ${x - 18} ${y} Z`} fill={c('amber-3')} />
			{[-130, -78, -26, 26, 78, 130].map((dx, i) => (
				<g key={i}>
					<path d={`M ${x + dx} ${y + 20} l -10 34 l 10 22 l 10 -22 Z`} fill={i % 2 ? c('sky-3') : c('bone-2')} />
					<rect x={x + dx - 6} y={y - 40} width={12} height={34} rx={3} fill={c('bone-2')} />
					<path d={`M ${x + dx} ${y - 70} q 9 14 0 26 q -9 -12 0 -26 Z`} fill={lit ? c('amber-3') : c('amber-4')} />
				</g>
			))}
		</g>
	);
}

function Hall({t, night, salon}: {t: number; night: boolean; salon: boolean}) {
	const wall = night ? c('violet-0') : salon ? c('kelp-3') : c('violet-4');
	const wallSh = night ? c('ink-1') : salon ? c('kelp-2') : c('violet-3');
	const panel = night ? c('violet-1') : salon ? c('kelp-4') : c('bone-1');
	const pil = night ? c('amber-2') : c('amber-4');
	const pilSh = night ? c('amber-0') : c('amber-2');
	const glass = night ? c('ink-2') : c('sky-2');
	const floor = night ? c('ochre-0') : c('ochre-2');
	const floorSh = night ? c('amber-0') : c('ochre-1');
	const horizon = 1040;
	const vx = 540;
	const vy = 640;
	return (
		<g>
			<rect width={W} height={H} fill={wall} />
			{/* ceiling + cornice */}
			<rect width={W} height={110} fill={wallSh} />
			<rect y={100} width={W} height={46} fill={pil} />
			<rect y={136} width={W} height={14} fill={pilSh} />
			{/* windows between pilasters */}
			{[150, 470, 790].map((x, i) => (
				<g key={i}>
					<path d={`M ${x} ${horizon - 170} V 420 A 80 80 0 0 1 ${x + 160} 420 V ${horizon - 170} Z`} fill={salon ? c('bone-2') : panel} />
					<path d={`M ${x + 14} ${horizon - 184} V 424 A 66 66 0 0 1 ${x + 146} 424 V ${horizon - 184} Z`} fill={glass} />
					{salon && !night && (
						<g>
							{/* Paris roofs through the window */}
							<path d={`M ${x + 14} ${horizon - 300} L ${x + 50} ${horizon - 340} L ${x + 90} ${horizon - 320} L ${x + 120} ${horizon - 360} L ${x + 146} ${horizon - 330} V ${horizon - 184} H ${x + 14} Z`} fill={c('dusk-3')} />
							<rect x={x + 40} y={horizon - 372} width={14} height={40} fill={c('bone-1')} />
						</g>
					)}
					{!salon && !night && <path d={`M ${x + 14} ${horizon - 250} q 40 -60 66 -10 q 30 -50 66 0 V ${horizon - 184} H ${x + 14} Z`} fill={c('kelp-1')} />}
					{night && i === 1 && <circle cx={x + 96} cy={500} r={34} fill={c('bone-1')} />}
					{night &&
						[0, 1, 2, 3].map((k) => (
							<circle key={k} cx={x + 30 + hash(i * 9 + k) * 100} cy={460 + hash(i * 5 + k + 2) * 280} r={4} fill={c('bone-1')}
								opacity={0.5 + 0.5 * Math.sin(t * 2 + k)} />
						))}
					<rect x={x + 76} y={380} width={8} height={horizon - 560} fill={salon ? c('bone-2') : panel} />
					<rect x={x + 14} y={640} width={132} height={8} fill={salon ? c('bone-2') : panel} />
				</g>
			))}
			{/* pilasters */}
			{[40, 360, 680, 1000].map((x) => (
				<g key={x}>
					<rect x={x} y={150} width={60} height={horizon - 150} fill={pil} />
					<rect x={x + 34} y={150} width={26} height={horizon - 150} fill={pilSh} />
					<rect x={x - 10} y={150} width={80} height={30} fill={pil} />
				</g>
			))}
			{/* wainscot */}
			<rect y={horizon - 150} width={W} height={150} fill={wallSh} />
			{[0, 1, 2, 3].map((i) => (
				<rect key={i} x={110 + i * 320} y={horizon - 128} width={200} height={100} rx={8} fill={panel} opacity={0.75} />
			))}
			<rect y={horizon - 18} width={W} height={18} fill={pilSh} />
			{/* floor: parquet planks toward the vanishing point */}
			<rect y={horizon} width={W} height={H - horizon} fill={floor} />
			{Array.from({length: 13}, (_, i) => {
				const xb = -900 + i * 240;
				const xt = vx + (xb - vx) * ((horizon - vy) / (H - vy));
				return <path key={i} d={`M ${f(xt)} ${horizon} L ${f(xb)} ${H} L ${f(xb + 90)} ${H} L ${f(xt + 90 * ((horizon - vy) / (H - vy)))} ${horizon} Z`} fill={floorSh} />;
			})}
			{/* carpet runner */}
			<path d={`M 440 ${horizon} L 640 ${horizon} L 1000 ${H} L 80 ${H} Z`} fill={night ? c('coral-0') : c('coral-1')} />
			<path d={`M 470 ${horizon} L 610 ${horizon} L 920 ${H} L 160 ${H} Z`} fill={night ? c('coral-1') : c('coral-2')} />
			<path d={`M 470 ${horizon} L 610 ${horizon} L 920 ${H} L 160 ${H} Z`} fill="none" stroke={c('amber-4')} strokeWidth={8} opacity={0.8} />
			<Chandelier x={540} y={310} t={t} lit={night} />
			{night && <rect width={W} height={H} fill={c('ink-1')} opacity={0.18} />}
		</g>
	);
}

function Facade({t}: {t: number}) {
	const base = 1120;
	const cloud = (x: number, y: number, s: number) => (
		<g transform={`translate(${f(x)} ${y}) scale(${s})`}>
			<path d="M -120 0 Q -120 -50 -70 -50 Q -50 -100 0 -90 Q 60 -110 80 -50 Q 130 -50 130 0 Z" fill={c('bone-2')} />
			<path d="M -120 0 L 130 0 Q 130 -24 108 -30 Q 0 -6 -110 -24 Z" fill={c('sky-4')} />
		</g>
	);
	return (
		<g>
			<rect width={W} height={H} fill={c('sky-2')} />
			<rect y={560} width={W} height={300} fill={c('sky-3')} />
			{cloud(220 + t * 8, 300, 1.1)}
			{cloud(860 - t * 6, 420, 0.8)}
			{/* palace wings */}
			<rect x={-40} y={620} width={W + 80} height={base - 620} fill={c('amber-4')} />
			<rect x={-40} y={600} width={W + 80} height={30} fill={c('bone-1')} />
			<path d={`M -40 600 L ${W + 40} 600 L ${W - 20} 540 L 20 540 Z`} fill={c('dusk-3')} />
			{/* central block */}
			<rect x={300} y={500} width={480} height={base - 500} fill={c('amber-4')} />
			<rect x={600} y={500} width={180} height={base - 500} fill={c('ochre-3')} />
			<path d="M 280 500 L 800 500 L 540 380 Z" fill={c('bone-1')} />
			<path d="M 540 380 L 800 500 L 540 500 Z" fill={c('bone-0')} />
			<path d="M 340 490 L 740 490 L 540 405 Z" fill={c('amber-3')} />
			{[330, 410, 490, 570, 650, 730].map((x) => (
				<g key={x}>
					<rect x={x} y={520} width={26} height={base - 600} fill={c('bone-2')} />
					<rect x={x + 14} y={520} width={12} height={base - 600} fill={c('bone-0')} />
				</g>
			))}
			{/* windows */}
			{[0, 1].map((row) =>
				Array.from({length: 14}, (_, i) => {
					const x = -10 + i * 80;
					if (x > 280 && x < 790) return null;
					const y = 680 + row * 190;
					return (
						<g key={`${row}-${i}`}>
							<rect x={x} y={y} width={46} height={120} rx={22} fill={c('bone-2')} />
							<rect x={x + 7} y={y + 8} width={32} height={106} rx={16} fill={c('sky-1')} />
						</g>
					);
				}),
			)}
			{/* door */}
			<path d={`M 490 ${base} V 1000 A 50 50 0 0 1 590 1000 V ${base} Z`} fill={c('ink-1')} />
			{/* courtyard */}
			<rect y={base} width={W} height={H - base} fill={c('ochre-4')} />
			<path d={`M 470 ${base} L 610 ${base} L 900 ${H} L 180 ${H} Z`} fill={c('ochre-3')} />
			{/* trees */}
			{[[90, 1040, 1.2], [1000, 1060, 1.1]].map(([x, y, s], i) => (
				<g key={i} transform={`translate(${x} ${y}) scale(${s})`}>
					<rect x={-12} y={-20} width={24} height={110} fill={c('ochre-0')} />
					<circle cx={0} cy={-90} r={90} fill={c('kelp-1')} />
					<path d="M 0 -180 A 90 90 0 0 1 0 0 A 70 90 0 0 0 0 -180 Z" fill={c('kelp-0')} />
				</g>
			))}
			{/* gate pillars in the foreground */}
			{[0, 1].map((i) => {
				const x = i ? 960 : 0;
				return (
					<g key={i}>
						<rect x={x} y={760} width={120} height={720} fill={c('bone-1')} />
						<rect x={x + (i ? 0 : 80)} y={760} width={40} height={720} fill={c('bone-0')} />
						<rect x={x - 14} y={740} width={148} height={40} fill={c('bone-0')} />
						<circle cx={x + 60} cy={712} r={34} fill={c('amber-4')} />
						<path d={`M ${x + 60} 678 A 34 34 0 0 1 ${x + 60} 746 A 24 34 0 0 0 ${x + 60} 678 Z`} fill={c('amber-2')} />
					</g>
				);
			})}
		</g>
	);
}

function Flame({x, y, s, t, k}: {x: number; y: number; s: number; t: number; k: number}) {
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

function Museum({t, fire}: {t: number; fire: number}) {
	const base = 1160;
	return (
		<g>
			<rect width={W} height={H} fill={c('ink-1')} />
			<rect y={700} width={W} height={500} fill={c('dusk-1')} />
			{Array.from({length: 18}, (_, i) => (
				<circle key={i} cx={hash(i) * W} cy={60 + hash(i + 40) * 560} r={3 + hash(i + 9) * 3} fill={c('bone-1')} opacity={0.5 + 0.4 * Math.sin(t * 2 + i)} />
			))}
			{fire > 0 && <circle cx={540} cy={700} r={700} fill={c('coral-1')} opacity={0.22 * fire} />}
			{/* smoke */}
			{fire > 0 &&
				Array.from({length: 7}, (_, i) => {
					const age = (t * 0.35 + i / 7) % 1;
					return (
						<circle key={i} cx={420 + i * 40 + Math.sin(t + i) * 30 + age * 120} cy={520 - age * 520} r={60 + age * 120}
							fill={c('ink-2')} opacity={fire * 0.85 * (1 - age)} />
					);
				})}
			{/* building */}
			<rect x={110} y={600} width={860} height={base - 600} fill={c('dusk-3')} />
			<rect x={640} y={600} width={330} height={base - 600} fill={c('dusk-2')} />
			<path d="M 80 600 L 1000 600 L 540 430 Z" fill={c('dusk-4')} />
			<path d="M 540 430 L 1000 600 L 540 600 Z" fill={c('dusk-3')} />
			<text x={540} y={570} textAnchor="middle" fill={c('bone-1')} fontFamily='"Anton", "Arial Narrow", sans-serif' fontSize={64} letterSpacing={8}>MUSEUM</text>
			{[150, 290, 430, 570, 710, 850].map((x) => (
				<g key={x}>
					<rect x={x} y={620} width={56} height={base - 640} fill={c('bone-0')} />
					<rect x={x + 30} y={620} width={26} height={base - 640} fill={c('sky-3')} />
				</g>
			))}
			{/* windows glowing with the fire */}
			{[220, 360, 500, 640, 780].map((x, i) => (
				<g key={x}>
					<rect x={x} y={700} width={60} height={150} rx={6} fill={fire > 0 ? c('amber-2') : c('ink-2')} />
					<rect x={x} y={930} width={60} height={150} rx={6} fill={fire > 0 ? c('amber-3') : c('ink-2')} />
					{fire > 0.2 && <Flame x={x + 30} y={850} s={0.55 * fire} t={t} k={i} />}
				</g>
			))}
			<rect x={70} y={base - 20} width={940} height={30} fill={c('dusk-4')} />
			{fire > 0 && [180, 340, 520, 700, 880].map((x, i) => <Flame key={i} x={x} y={600 - (i % 2) * 20} s={(1.2 + (i % 3) * 0.3) * fire} t={t} k={i + 5} />)}
			{fire > 0 && <Flame x={540} y={440} s={1.6 * fire} t={t} k={11} />}
			{/* street */}
			<rect y={base} width={W} height={H - base} fill={c('ink-2')} />
			<rect y={base} width={W} height={24} fill={c('dusk-1')} />
			{fire > 0 &&
				Array.from({length: 14}, (_, i) => {
					const age = (t * 0.6 + hash(i)) % 1;
					return <circle key={i} cx={200 + hash(i + 3) * 700 + Math.sin(t * 3 + i) * 20} cy={700 - age * 600} r={6} fill={c('amber-4')} opacity={(1 - age) * fire} />;
				})}
		</g>
	);
}

function Blueprint({t}: {t: number}) {
	return (
		<g>
			<rect width={W} height={H} fill={c('tide-0')} />
			{Array.from({length: 12}, (_, i) => (
				<rect key={`v${i}`} x={i * 96} y={0} width={3} height={H} fill={c('tide-1')} />
			))}
			{Array.from({length: 21}, (_, i) => (
				<rect key={`h${i}`} x={0} y={i * 96} width={W} height={3} fill={c('tide-1')} />
			))}
			<circle cx={540} cy={760} r={620 + Math.sin(t) * 6} fill={c('tide-1')} opacity={0.35} />
		</g>
	);
}

export const StickSet: React.FC<KitComponentProps> = ({props, time}) => {
	const place = str(props.place, 'hall');
	const fire = clamp(track(props.fire, time, 0));
	return (
		<svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
			{place === 'hall' && <Hall t={time} night={false} salon={false} />}
			{place === 'hallNight' && <Hall t={time} night salon={false} />}
			{place === 'salon' && <Hall t={time} night={false} salon />}
			{place === 'facade' && <Facade t={time} />}
			{place === 'museum' && <Museum t={time} fire={fire} />}
			{place === 'blueprint' && <Blueprint t={time} />}
		</svg>
	);
};
