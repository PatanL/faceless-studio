import React from 'react';
import {Cam, E, blinking, camAt, camT, clamp, look, rng} from '../lib/anim';
import {GunPose, gunPt} from '../art/guns';
import {Look, LOOKS, Soldier} from '../art/soldier';
import {CloudBand, Streaks, streakSet} from '../art/props';

// Scene block 5 (25.97-32.80): grey ruined city. S14 squad line, S15 ECU on the selector, S16 tilt up to E.

const STREET = streakSet(14, 26, -800, 2000, 980, 2600, 160, 520, 30);
const CLOUDS: [number, number, number][] = [
	[100, 160, 1.4],
	[520, 90, 1.2],
	[900, 220, 1.1],
	[1300, 120, 1.3],
];
// v3 acting: each squad member has his own stance, lean, gun angle, head tilt and step phase (no clone line)
type Member = {look: Look; x: number; crouch: number; lean: number; gunRot: number; gunY: number; tilt: number; stance: number; phase: number; speed: number; brows: 'neutral' | 'angry' | 'worried' | 'raised'; mouth: 'closed' | 'flat' | 'o'};
const SQUAD: Member[] = [
	{look: LOOKS.B, x: 270, crouch: 0.7, lean: 7, gunRot: 9, gunY: 10, tilt: -6, stance: 6, phase: 0, speed: 1.6, brows: 'neutral', mouth: 'closed'},
	{look: LOOKS.A, x: 478, crouch: 0.4, lean: 3, gunRot: -3, gunY: -14, tilt: 5, stance: -8, phase: 0.31, speed: 1.5, brows: 'angry', mouth: 'flat'},
	{look: LOOKS.E, x: 680, crouch: 0.6, lean: 4, gunRot: 4, gunY: 0, tilt: -2, stance: 0, phase: 0.62, speed: 1.6, brows: 'neutral', mouth: 'closed'},
	{look: LOOKS.Blond, x: 885, crouch: 0.85, lean: 10, gunRot: 14, gunY: 22, tilt: 8, stance: 14, phase: 0.85, speed: 1.7, brows: 'worried', mouth: 'o'},
];
const SY = 1170;
const SS = 0.91;
const EI = 2;

function squadGun(i: number, t: number, bob: number): GunPose {
	const m = SQUAD[i];
	return {kind: 'ak12', x: 70 - m.gunY * 0.4, y: -300 + m.gunY + bob * 0.3, rot: m.gunRot + Math.sin(t * 4 + i) * 1.5, lod: i === EI ? 2 : 1};
}
const march = (t: number, i: number) => t * SQUAD[i].speed + SQUAD[i].phase;

/** World position of E's receiver centre (the S15 ECU subject). */
function eRecv(t: number): [number, number] {
	const g = squadGun(EI, t, 0);
	return [SQUAD[EI].x + SS * (g.x - 4), SY + SS * (g.y + 26)];
}

const Tower: React.FC = () => {
	const R = rng(4);
	const wins = [];
	for (let r = 0; r < 6; r++)
		for (let c = 0; c < 3; c++) {
			const x = 700 + c * 140;
			const y = -60 + r * 170;
			const broken = R() < 0.35;
			wins.push(
				<g key={`${r}${c}`}>
					<rect x={x} y={y} width={92} height={120} fill="#201940" />
					<rect x={x + 44} y={y} width={6} height={120} fill={broken ? '#5A4A40' : '#E2D5BA'} opacity={broken ? 1 : 0.7} transform={broken ? `rotate(14 ${x + 47} ${y + 60})` : undefined} />
					<rect x={x} y={y + 54} width={92} height={6} fill="#E2D5BA" opacity={0.7} />
					<rect x={x - 6} y={y + 120} width={104} height={10} fill="#CFC0A2" />
				</g>,
			);
		}
	const bricks = [];
	for (let i = 0; i < 24; i++) bricks.push(<rect key={i} x={660 + R() * 460} y={-80 + R() * 1000} width={36} height={14} rx={3} fill="#C9B691" />);
	return (
		<g>
			<rect x={640} y={-400} width={600} height={1360} fill="#E2D5BA" />
			<rect x={640} y={-400} width={30} height={1360} fill="#F0E6D0" />
			{bricks}
			{wins}
			<path d="M760,120 L800,190 L790,260 L840,330 M980,400 L1020,460 L1010,560 L1060,620 M720,640 L700,720 L740,790" stroke="#7B675D" strokeWidth={5} fill="none" strokeLinecap="round" />
		</g>
	);
};

const Rebar: React.FC = () => (
	<g>
		{/* distant blue-grey ruin + mauve wall */}
		<path d="M100,960 L100,260 L170,260 L190,130 L230,250 L330,250 L360,180 L420,260 L460,260 L460,960 Z" fill="#4A555C" />
		<path d="M190,130 L200,40 L214,120 Z" fill="#4A555C" />
		<path d="M-200,960 L-200,320 L40,280 L140,340 L150,960 Z" fill="#8E6A73" />
		<rect x={-40} y={420} width={120} height={300} fill="#201940" />
		<path d="M-200,320 L40,280 L50,300 L-200,340 Z" fill="#A98690" />
		{/* twisted rebar frame */}
		{[
			[160, 420, 520, 340, '#7B4B4B'],
			[200, 600, 560, 560, '#7B4B4B'],
			[300, 260, 340, 900, '#5C3A3A'],
			[460, 320, 430, 900, '#5C3A3A'],
			[180, 520, 260, 300, '#7B4B4B'],
			[540, 420, 600, 920, '#5C3A3A'],
		].map(([x1, y1, x2, y2, c], i) => (
			<g key={i}>
				<line x1={x1} y1={y1} x2={x2} y2={y2} stroke={c as string} strokeWidth={30} strokeLinecap="round" />
				<line x1={x1 as number} y1={(y1 as number) - 6} x2={x2 as number} y2={(y2 as number) - 6} stroke="#A06A60" strokeWidth={6} strokeLinecap="round" opacity={0.6} />
			</g>
		))}
		{/* rubble mound */}
		<path d="M60,980 Q200,800 380,830 Q520,760 700,900 L760,980 Z" fill="#D6C29C" />
		<path d="M200,860 L260,830 L300,870 Z M420,820 L470,800 L500,840 Z" fill="#B8A27C" />
	</g>
);

function cam(t: number): Cam {
	const h = eRecv(t);
	const eFace: [number, number] = [SQUAD[EI].x + 10 * SS, SY - (474 + 67) * SS];
	return camAt(t, [
		[25.97, {x: 540, y: 960, s: 1, r: 0}],
		[26.6, {x: 545, y: 960, s: 1.04, r: 0}, E.linear],
		[28.0, look(h, [560, 900], 1.9, 1), E.inCubic],
		// S15: the grey receiver fills the frame, the selector lever under the fumbling hand
		[28.8, look(h, [560, 960], 4.7, 2), E.outCubic],
		[30.4, look([h[0] - 6, h[1] + 4], [580, 980], 4.85, 2), E.linear],
		// S16: tilt up to a big E, grimacing, the rifle crossing the foreground
		// v3: E stays smaller on the tilt, the oversized hand stays big in the foreground
		[31.2, look([eFace[0] + 30, eFace[1] + 90], [560, 640], 2.7, -6), E.inOutCubic],
		[32.9, look([eFace[0] + 30, eFace[1] + 90], [560, 640], 2.8, -7), E.linear],
	]);
}

export const Ruins: React.FC<{t: number}> = ({t}) => {
	const c = cam(t);
	const fumble = t > 28.6 && t < 30.6;
	// the S15 gag: E's hand balloons into a huge fumbling circle over the receiver (and stays big into S16)
	const bigHand = 1 + 0.85 * Math.min(E.outBack(clamp((t - 28.25) / 0.45)), 1 - E.inOutCubic(clamp((t - 32.2) / 0.3)));
	return (
		<g>
			<g transform={camT(c)}>
				<rect x={-800} y={-800} width={2800} height={1800} fill="#B1D6EA" />
				<CloudBand t={t} items={CLOUDS} w={1800} x0={-300} c="#F7FBFD" sh="#C7E1F0" />
				<Rebar />
				<Tower />
				<rect x={-800} y={950} width={2800} height={2000} fill="#7F92A7" />
				<Streaks items={STREET} c="#8FA1B4" />
				{SQUAD.map((m, i) => {
					const ph = march(t, i);
					const bob = Math.abs(Math.sin(ph * Math.PI * 2)) * 6;
					const g = squadGun(i, t, bob);
					const isE = i === EI;
					const hN: [number, number] | 'grip' =
						isE && fumble
							? (() => {
									// thumb hunts for the selector lever: grip -> lever -> slips back, repeated
									const p = gunPt(g, 'grip');
									const q = gunPt(g, 'sel');
									const v = 0.5 + 0.5 * Math.sin((t - 28.6) * Math.PI * 2 * 0.9 - Math.PI / 2);
									const k = Math.floor(t * 5);
									return [p[0] + (q[0] + 18 - p[0]) * v + Math.sin(t * 9) * 5, p[1] + (q[1] + 30 - p[1]) * v + (k % 2 ? 3 : -2)] as [number, number];
								})()
							: 'grip';
					const talking = isE && t > 30.6;
					const grimace = talking ? (t % 0.42 < 0.28 ? 'yell' : 'grin') : null;
					return (
						<Soldier
							key={i}
							look={m.look}
							x={m.x}
							y={SY}
							s={SS}
							pose={{
								facing: 1,
								legs: 'march',
								legPhase: ph,
								crouch: m.crouch,
								stance: m.stance,
								bob: -bob,
								lean: m.lean,
								gun: g,
								handN: hN,
								handNScale: isE ? bigHand : 1,
								handF: 'fore',
								mouth: grimace ?? m.mouth,
								brows: talking ? 'angry' : m.brows,
								eyes: blinking(t, 30 + i) ? 'closed' : 'open',
								headRot: m.tilt + Math.sin(t * 1.3 + i * 2) * 4,
								headX: i === 3 ? 6 : 0,
								lookX: Math.sin(t * 0.9 + i) * 2.5,
								breathe: t * 0.4,
							}}
						/>
					);
				})}
			</g>
		</g>
	);
};
