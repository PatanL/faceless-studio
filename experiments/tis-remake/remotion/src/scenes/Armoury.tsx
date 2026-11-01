import React from 'react';
import {E, blinking, camAt, camT, clamp, kf, look, talkMouth} from '../lib/anim';
import {GunPose} from '../art/guns';
import {LOOKS, Soldier} from '../art/soldier';
import {Streaks, streakSet} from '../art/props';

// Scene block 7 (38.55-44.80): the armoury. S20 queue + quartermaster, S21 push to B with his new rifle.

const WALL = streakSet(41, 22, -400, 1500, -300, 1050, 160, 420, 70);
const FLOOR = streakSet(43, 14, -400, 1500, 1140, 2200, 120, 360, 24);

const Bag: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
	<g transform={`translate(${x} ${y}) scale(${s})`}>
		<path d="M-46,0 Q-54,-60 -20,-74 L20,-74 Q54,-60 46,0 Z" fill="#6E8E3A" />
		<path d="M10,-74 L20,-74 Q54,-60 46,0 L20,0 Q34,-40 10,-74 Z" fill="#4F6B2A" />
		<path d="M-20,-74 Q0,-92 20,-74 L14,-66 Q0,-76 -14,-66 Z" fill="#4F6B2A" />
		<rect x={-30} y={-50} width={22} height={8} rx={4} fill="#88A852" />
	</g>
);
const Box: React.FC<{x: number; y: number; w: number; h: number}> = ({x, y, w, h}) => (
	<g>
		<rect x={x} y={y} width={w} height={h} rx={4} fill="#C39D60" />
		<rect x={x} y={y} width={w} height={h * 0.18} fill="#8B7953" opacity={0.7} />
		<rect x={x + w * 0.42} y={y} width={w * 0.16} height={h} fill="#D8B47A" opacity={0.6} />
		<rect x={x + w - 10} y={y} width={10} height={h} fill="#000" opacity={0.1} />
	</g>
);

const Rack: React.FC<{x: number; w: number}> = ({x, w}) => (
	<g>
		{[322, 578, 832].map((y, i) => (
			<g key={y}>
				{i % 2 === 0 ? (
					<>
						<Bag x={x + w * 0.3} y={y} />
						<Bag x={x + w * 0.7} y={y} s={0.9} />
					</>
				) : (
					<>
						<Box x={x + 14} y={y - 110} w={w * 0.45} h={110} />
						<Box x={x + w * 0.5} y={y - 90} w={w * 0.42} h={90} />
					</>
				)}
			</g>
		))}
		<Box x={x + 14} y={980} w={w * 0.8} h={108} />
		<rect x={x} y={180} width={18} height={930} fill="#2B231E" />
		<rect x={x + w - 18} y={180} width={18} height={930} fill="#2B231E" />
		{[322, 578, 832, 1088].map((y) => (
			<g key={y}>
				<rect x={x - 10} y={y} width={w + 20} height={26} fill="#F2C12E" />
				<rect x={x - 10} y={y} width={w + 20} height={7} fill="#F8D866" />
			</g>
		))}
	</g>
);

const OX = 830;
const FY = 1185;
const SS = 1.04;

export const Armoury: React.FC<{t: number}> = ({t}) => {
	const bFace: [number, number] = [532 + 10 * SS, FY - 541 * SS];
	// S21: a clean MCU of B (A's face is pushed out of frame left, the officer is only a shoulder at right)
	const c = camAt(t, [
		[38.55, {x: 540, y: 960, s: 1, r: 0}],
		[40.5, {x: 548, y: 958, s: 1.03, r: 0}, E.linear],
		[41.8, look(bFace, [360, 600], 2.85, 6), E.inOutCubic],
		[44.9, look([bFace[0] + 8, bFace[1] + 8], [360, 600], 2.95, 7), E.linear],
	]);
	// the rifle: slides across the table, lifted, then B holds it (S21)
	const slide = E.inOutCubic(clamp((t - 39.3) / 0.7));
	const lift = E.inOutCubic(clamp((t - 40.0) / 0.5));
	const gx = kf(t, [
		[39.3, 960],
		[40.0, 760],
		[40.5, 700],
	]);
	const gy = 925 - lift * 120;
	// officer local gun (officer faces -1, leans over)
	const oGun: GunPose | null = t < 41.0 ? {kind: 'ak12', x: (OX - gx) / SS, y: (gy - FY) / SS, rot: 180 + lift * 10} : null;
	const bHas = t >= 41.0;
	// B takes the rifle low and swings it up to a clear diagonal with an overshoot-and-settle
	const up = E.outBack(clamp((t - 41.0) / 0.6));
	const bGun: GunPose = {kind: 'ak12', x: 40 + (1 - up) * 30, y: -350 + (1 - up) * 40 + Math.sin(t * 2) * 4, rot: -18 - up * 40, lod: 2};
	const scratch = Math.sin(t * Math.PI * 2 * 1.4);
	return (
		<g>
			<g transform={camT(c)}>
				<rect x={-600} y={-600} width={2400} height={1740} fill="#E6C394" />
				<Streaks items={WALL} c="#EDCCA4" />
				<Streaks items={WALL.slice(0, 8).map(([x, y, w, h]) => [x + 60, y + 40, w * 0.7, h * 0.6] as [number, number, number, number])} c="#EDD5AE" />
				<Rack x={-30} w={250} />
				<Rack x={975} w={260} />
				<rect x={-600} y={1110} width={2400} height={1400} fill="#C39D60" />
				<Streaks items={FLOOR} c="#CDA96E" />
				{/* officer behind the table */}
				<Soldier
					look={LOOKS.Off}
					x={OX}
					y={FY}
					s={SS}
					pose={{
						facing: -1,
						lean: 14,
						gun: oGun,
						handN: oGun ? 'grip' : [40, -330],
						handF: oGun ? 'fore' : [90, -320],
						mouth: t > 39.4 && t < 40.6 ? talkMouth(t, 8, 'flat') : 'flat',
						brows: 'angry',
						eyes: blinking(t, 61) ? 'closed' : 'open',
						lookX: 2,
						lookY: 1.5,
						breathe: t * 0.4,
					}}
				/>
				{/* table + kit */}
				<rect x={640} y={940} width={430} height={30} rx={6} fill="#DDB07D" />
				<rect x={640} y={940} width={430} height={8} rx={4} fill="#EBC895" />
				<rect x={660} y={970} width={22} height={220} fill="#C39D60" />
				<rect x={1030} y={970} width={22} height={220} fill="#C39D60" />
				<rect x={660} y={970} width={392} height={14} fill="#000" opacity={0.12} />
				{[0, 1, 2].map((i) => (
					<rect key={i} x={680} y={900 - i * 22} width={150} height={24} rx={8} fill="url(#camoRU)" />
				))}
				<Bag x={930} y={942} s={1.05} />
				<Bag x={1010} y={942} s={0.9} />
				{/* the queue */}
				<Soldier look={LOOKS.D} x={172} y={FY} s={SS} pose={{facing: 1, mouth: 'flat', brows: 'neutral', eyes: blinking(t, 62) ? 'closed' : 'open', breathe: t * 0.4, headRot: Math.sin(t * 1.1) * 2, lookX: 2.2}} />
				<Soldier look={LOOKS.A} x={352} y={FY} s={SS} pose={{facing: 1, mouth: talkMouth(t, 9, 'closed'), brows: 'neutral', eyes: blinking(t, 63) ? 'closed' : 'open', breathe: t * 0.4 + 0.5, headRot: Math.sin(t * 4) * 2, lookX: 2.4}} />
				<Soldier
					look={LOOKS.B}
					x={532}
					y={FY}
					s={SS}
					pose={{
						facing: 1,
						gun: bHas ? bGun : null,
						handN: bHas ? 'grip' : undefined,
						handF: bHas ? 'fore' : t < 40.4 ? [20 + scratch * 6, -600 + scratch * 14] : [110, -330],
						mouth: bHas ? talkMouth(t, 10, 'O') : 'O',
						brows: 'worried',
						eyes: blinking(t, 64) ? 'closed' : 'open',
						headRot: bHas ? Math.sin(t * 0.8) * 4 - 2 : -3,
						breathe: t * 0.4 + 0.2,
						lookX: 2,
					}}
				/>
			</g>
		</g>
	);
};
