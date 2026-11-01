import React from 'react';
import {Cam, E, FPS, blinking, camAt, camT, clamp, look, para, talkMouth} from '../lib/anim';
import {GunPose, gunPt} from '../art/guns';
import {LOOKS, Soldier} from '../art/soldier';
import {CloudBand, MuzzleFlash, Streaks, Target, streakSet} from '../art/props';
import {Cap} from '../art/defs';

// Scene block 3 (13.95-22.30): firing range. S08 shooter, S09 truck right, S10 target, S11 D pops in, S12 push + heart eyes.

const SAND = streakSet(8, 40, -600, 3400, 600, 2600, 160, 560, 34);
const CLOUDS: [number, number, number][] = [
	[1500, 40, 0.8],
	[1900, 10, 0.7],
	[2300, 50, 0.9],
	[2700, 20, 0.7],
];

const CX = 330;
const CY = 1185;
const CS = 1.3;

/** Gun of the kneeling shooter with recoil (torso frame). */
function shooterGun(t: number): GunPose {
	const f = Math.floor(t * FPS);
	const k = Math.floor(f / 2.5);
	const firing = k % 4 !== 3;
	const kick = firing ? (f % 3 === 0 ? 9 : 4) : 0;
	return {kind: 'ak12', x: 176 - kick, y: -448, rot: -2 + (kick ? -1.2 : 0), lod: 2};
}

/** Soldier C kneeling and firing, in local coords (feet at 0,0, unit scale). Also used as the S07->S08 matte. */
export const SHOOTER: React.FC<{t: number; silhouette?: boolean}> = ({t, silhouette}) => {
	const g = shooterGun(t);
	const f = Math.floor(t * FPS);
	const m = gunPt(g, 'muzzle');
	const torsoDY = 105;
	const kick = g.x < 176 ? 2 : 0;
	return (
		<g>
			<Soldier
				look={LOOKS.C}
				x={0}
				y={0}
				shadow={!silhouette}
				pose={{
					facing: 1,
					legs: 'kneel',
					gun: g,
					handN: 'grip',
					handF: 'fore',
					brows: 'angry',
					mouth: 'flat',
					lean: 6 - kick,
					headX: 14 - kick,
					headY: 6,
					headRot: 4,
					eyes: blinking(t, 9) ? 'closed' : 'open',
					lookX: 2.5,
				}}
			/>
			<g transform={`translate(${m[0] + 34} ${m[1] + torsoDY - 4})`}>
				<MuzzleFlash frame={f} size={205} seed={1} />
			</g>
			{!silhouette &&
				[0, 1, 2].map((i) => {
					const age = ((t * 3 + i / 3) % 1) * 0.6;
					return <Cap key={i} x={40 + age * 220} y={-470 - age * 260 + age * age * 500} w={14} h={7} fill="#E3B23C" />;
				})}
		</g>
	);
};

const Hangar: React.FC = () => {
	const ribs = [];
	for (let x = -400; x < 1780; x += 34) ribs.push(<rect key={x} x={x} y={-900} width={8} height={1432} fill={x % 68 === 0 ? '#DFD1C2' : '#BAB297'} />);
	const posts = [];
	for (let x = -400; x < 1780; x += 64) posts.push(<rect key={x} x={x} y={532} width={34} height={38} fill="#3C372E" />);
	return (
		<g>
			{/* left arched end + wall */}
			<rect x={-400} y={-900} width={2180} height={1440} fill="#C8C0A5" />
			{ribs}
			<path d="M-400,520 Q-320,-160 260,-900 L-400,-900 Z" fill="#A08A6B" />
			<path d="M-400,520 Q-330,-170 250,-900 L232,-900 Q-350,-150 -420,520 Z" fill="#4A3F35" />
			{/* roller door */}
			<rect x={590} y={92} width={440} height={60} fill="#4A3F35" />
			<rect x={597} y={150} width={426} height={382} fill="#B99F7A" />
			{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
				<rect key={i} x={597} y={168 + i * 46} width={426} height={7} fill="#9F8462" />
			))}
			<Cap x={650} y={196} w={120} h={30} fill="#C8AE89" />
			<Cap x={830} y={330} w={150} h={30} fill="#C8AE89" />
			<Cap x={700} y={430} w={90} h={30} fill="#C8AE89" />
			{/* second door far right */}
			<rect x={1300} y={92} width={300} height={60} fill="#4A3F35" />
			<rect x={1306} y={150} width={288} height={382} fill="#B99F7A" />
			{[0, 1, 2, 3, 4, 5, 6, 7].map((i) => (
				<rect key={i} x={1306} y={168 + i * 46} width={288} height={7} fill="#9F8462" />
			))}
			{/* plinth */}
			<rect x={-400} y={520} width={2180} height={50} fill="#4D463A" />
			{posts}
			{/* bay signs */}
			<rect x={315} y={172} width={132} height={60} rx={6} fill="#FFFFFF" />
			<text x={381} y={218} textAnchor="middle" fontFamily="MontserratXB" fontWeight={800} fontSize={44} fill="#222">
				270
			</text>
			<rect x={1160} y={150} width={84} height={84} rx={12} fill="#FFFFFF" />
			<text x={1202} y={213} textAnchor="middle" fontFamily="MontserratXB" fontWeight={800} fontSize={64} fill="#222">
				A
			</text>
			{/* right arched end */}
			<path d="M1780,532 Q1760,-200 1500,-900 L1780,-900 Z" fill="#A08A6B" />
			<path d="M1780,532 Q1758,-200 1500,-900 L1520,-900 Q1780,-200 1800,532 Z" fill="#4A3F35" />
		</g>
	);
};

const Far: React.FC = () => (
	<g>
		{/* fence on the horizon */}
		{Array.from({length: 40}, (_, i) => (
			<rect key={i} x={1500 + i * 60} y={70} width={8} height={70} fill="#5A5148" />
		))}
		<rect x={1500} y={86} width={2400} height={4} fill="#5A5148" />
		<rect x={1500} y={110} width={2400} height={4} fill="#5A5148" />
		{/* lifeguard-style tower + watchtower post */}
		<g transform="translate(1880 140)">
			<rect x={-70} y={-220} width={140} height={20} fill="#6E5A3A" />
			<rect x={-60} y={-280} width={120} height={60} fill="none" stroke="#6E5A3A" strokeWidth={12} />
			<path d="M-60,-200 L-80,0 M60,-200 L80,0 M-70,-100 L70,-100" stroke="#6E5A3A" strokeWidth={14} />
			<path d="M-70,-220 L-30,-170 M70,-220 L30,-170" stroke="#5A4A30" strokeWidth={8} />
		</g>
		<rect x={2380} y={-400} width={44} height={520} fill="#3C372E" />
		<rect x={2380} y={-400} width={12} height={520} fill="#56503F" />
		<g transform="translate(2900 140)">
			<rect x={-70} y={-220} width={140} height={20} fill="#6E5A3A" />
			<path d="M-60,-200 L-80,0 M60,-200 L80,0 M-70,-100 L70,-100" stroke="#6E5A3A" strokeWidth={14} />
		</g>
	</g>
);

function cam(t: number): Cam {
	const dFace: [number, number] = [2253, 300];
	return camAt(t, [
		[13.95, {x: 540, y: 960, s: 1, r: 0}],
		[16.0, {x: 540, y: 960, s: 1, r: 0}],
		[17.05, {x: 1950, y: 960, s: 1, r: 0}, E.inOutCubic],
		[17.4, {x: 1940, y: 960, s: 1, r: 0}, E.inOutSine],
		[19.9, {x: 1952, y: 960, s: 1.02, r: 0}, E.linear],
		[21.1, look(dFace, [600, 640], 2.3, 8), E.inOutCubic],
		[22.4, look([dFace[0] + 8, dFace[1] + 6], [600, 640], 2.36, 8.5), E.linear],
	]);
}

export const Range: React.FC<{t: number}> = ({t}) => {
	const c = cam(t);
	const cf = para(c, 0.6, 1950, 960);
	// target: y-turn toward camera 17.0-17.4, two holes per burst
	const tq = 0.85 + 0.15 * E.outCubic(clamp((t - 17.0) / 0.4));
	const holes: [number, number, number][] = [
		[-60, -80, 0],
		[90, 40, 0],
		[-130, 120, 0],
		[30, -150, 0],
		[150, -60, 17.5],
		[-40, 60, 17.57],
		[60, 170, 18.0],
		[-170, -40, 18.07],
	];
	// D grows from a dot 18.23-18.60, raises rifle from 19.25, hugs from 20.3
	const dk = E.outCubic(clamp((t - 18.23) / 0.37));
	const raise = E.outBack(clamp((t - 19.25) / 0.45));
	const hug = E.outBack(clamp((t - 20.3) / 0.6));
	const dGun: GunPose = {kind: 'ak12acc', x: 70 + raise * 6 - hug * 40, y: -300 - raise * 90 - hug * 20, rot: -4 - raise * 22 - hug * 30, lod: 2};
	const hearts = t >= 20.25;
	return (
		<g>
			<g transform={camT(cf)}>
				<rect x={-1000} y={-2000} width={6000} height={2200} fill="#D0E5FA" />
				<CloudBand t={t} items={CLOUDS} w={1800} x0={1300} />
				<Far />
			</g>
			<g transform={camT(c)}>
				<rect x={-1000} y={130} width={6000} height={3000} fill="#CCB69A" />
				<Streaks items={SAND} c="#DFD2C3" />
				<Hangar />
				<g transform={`translate(${CX} ${CY}) scale(${CS})`}>
					<SHOOTER t={t} />
				</g>
				{/* target */}
				<g transform={`translate(1895 640) scale(${1.09 * tq} 1.09)`}>
					<ellipse cx={0} cy={560} rx={260} ry={26} fill="url(#softShadow)" />
					<Target holes={holes} t={t} />
				</g>
				{/* D */}
				{t >= 18.23 && (
					<g transform={`translate(2270 1200) scale(${Math.max(0.001, dk)})`}>
						<Soldier
							look={LOOKS.D}
							x={0}
							y={0}
							s={1.67}
							pose={{
								facing: -1,
								gun: dGun,
								handN: 'grip',
								handF: 'fore',
								eyes: hearts ? 'hearts' : blinking(t, 13) ? 'closed' : 'open',
								heartPulse: 1 + 0.075 * (1 + Math.sin(t * Math.PI * 2 * 3)),
								mouth: hearts ? 'smile' : t > 18.8 ? talkMouth(t, 4, 'flat') : 'flat',
								brows: hearts ? 'happy' : 'neutral',
								breathe: t * 0.45,
								headRot: hearts ? Math.sin(t * 3) * 3 - 4 : 0,
								lookX: 2,
							}}
						/>
					</g>
				)}
			</g>
		</g>
	);
};
