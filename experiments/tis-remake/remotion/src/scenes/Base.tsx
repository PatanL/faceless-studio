import React from 'react';
import {Cam, E, blinking, camAt, camT, clamp, kf, look, talkMouth} from '../lib/anim';
import {GunPose} from '../art/guns';
import {LOOKS, Soldier} from '../art/soldier';
import {Calendar, Clipboard, CloudBand, LatticeTower, PoleFlag, Quonset, Sparkle, Streaks, streakSet} from '../art/props';
import {P} from '../art/defs';

// Scene block 2 (2.87-14.25): Russian base. One set, the camera travels inside it (S02-S07).

const AX = 795;
const BX = 322;
const FY = 1185;
const GRASS = streakSet(3, 16, -900, 2000, 690, 1000, 120, 380, 22);
const DIRT = streakSet(5, 22, -900, 2000, 1230, 2600, 140, 420, 30);
const CLOUDS: [number, number, number][] = [
	[-200, 300, 1.1],
	[260, 180, 0.9],
	[700, 330, 1.2],
	[1150, 140, 1.0],
	[1500, 380, 0.9],
	[40, 520, 0.8],
];

/** A's gun + hands over time (torso frame, A faces -1 so +x points toward B). */
function aGun(t: number): GunPose {
	// hold AK-47 across the chest
	if (t < 6.9) {
		const sway = Math.sin(t * 2.1) * 2;
		return {kind: 'ak47', x: 8, y: -352 + Math.sin(t * 2.1) * 3, rot: -42 + sway};
	}
	if (t < 7.6) {
		const u = E.inOutCubic(clamp((t - 6.9) / 0.7));
		return {kind: 'ak47', x: 8 + u * 10, y: -352 - u * 70, rot: -42 - u * 38};
	}
	if (t < 8.3) {
		const u = E.inCubic(clamp((t - 7.6) / 0.7));
		return {kind: 'ak47', x: 18 - u * 260, y: -422 - u * 820, rot: -80 - u * 10};
	}
	// AK-12 comes back down (S05), CU in S06, lifted out 10.75-11.30
	if (t < 9.0) {
		const u = E.outCubic(clamp((t - 8.3) / 0.7));
		return {kind: 'ak12', x: -230 + u * 236, y: -1240 + u * 880, rot: -90 + u * 40};
	}
	if (t < 10.75) {
		const u = clamp((t - 9.0) / 1.75);
		return {kind: 'ak12', x: 6 + u * 6, y: -360 - u * 14, rot: -50 + u * 5};
	}
	const u = E.inCubic(clamp((t - 10.75) / 0.55));
	return {kind: 'ak12', x: 12 - u * 240, y: -374 - u * 760, rot: -45 - u * 20};
}

function cam(t: number): Cam {
	const aFace: [number, number] = [AX - 10, FY - 537];
	const aChest: [number, number] = [AX - 10, FY - 360];
	const bFace: [number, number] = [BX + 10, FY - 537];
	return camAt(t, [
		[2.87, look(aFace, [760, 640], 2.7, 18)],
		[4.5, look(aFace, [760, 640], 2.8, 17), E.linear],
		[5.6, {x: 540, y: 960, s: 1, r: 2}, E.inOutCubic],
		[8.1, {x: 545, y: 955, s: 1.02, r: 2}, E.linear],
		[9.0, look([aChest[0], aChest[1] + 60], [560, 780], 3.9, 17), E.inOutCubic],
		[11.3, look([aChest[0] + 25, aChest[1] + 90], [520, 720], 4.1, 19), E.linear],
		[11.5, look([aChest[0] + 25, aChest[1] + 90], [520, 720], 4.1, 19), E.linear],
		[11.9, look(bFace, [70, 700], 3.3, 6), E.inOutCubic],
		[14.3, look(bFace, [70, 700], 3.43, 6), E.linear],
	]);
}

export const Base: React.FC<{t: number}> = ({t}) => {
	const c = cam(t);
	const g = aGun(t);
	const aTalk = t < 5.6 || (t > 9 && t < 11.3);
	const aMouth = aTalk ? talkMouth(t, 1) : 'closed';
	const bTalking = t > 5.6 && t < 8.1;
	// B points with two stabs (5.9-6.3, 6.4-6.8)
	const stab = kf(t, [
		[5.7, 0],
		[5.95, 1],
		[6.15, 0.55],
		[6.4, 1],
		[6.6, 0.6],
	]);
	const bPoint: [number, number] = [70 + stab * 40, -400 - stab * 18];
	const tick = [12.25, 12.75, 13.25];
	const nod = tick.reduce((acc, tc) => acc + (t > tc && t < tc + 0.4 ? Math.sin(((t - tc) / 0.4) * Math.PI) * 4 : 0), 0);
	const bMouth = t > 11.3 ? (Math.floor(t * 3) % 3 === 0 ? 'smile' : 'grin') : bTalking ? talkMouth(t, 3, 'flat') : 'flat';
	return (
		<g>
			<g transform={camT(c)}>
				{/* sky + clouds */}
				<rect x={-1500} y={-1500} width={4200} height={2200} fill={P.sky} />
				<ellipse cx={420} cy={720} rx={760} ry={360} fill="#E4EFF9" opacity={0.7} />
				<CloudBand t={t} items={CLOUDS} w={2200} x0={-700} />
				{/* back hut + tower */}
				<Quonset x={70} y={700} w={360} h={300} c="#69654C" rim="#8E8964" dark="#3E3C2C" door="#333332" strut="#53533D" doorW={130} />
				<LatticeTower x={1020} y={690} w={170} h={640} levels={5} />
				{/* flags */}
				<PoleFlag x={535} y={470} h={390} fw={310} kind="ru" t={t} />
				<PoleFlag x={68} y={520} h={300} fw={200} kind="ru" t={t} seed={1.7} />
				{/* grass, dirt, path, ground */}
				<rect x={-1500} y={645} width={4200} height={380} fill="#A9B281" />
				<Streaks items={GRASS} c="#B5BD8F" />
				<rect x={-1500} y={1020} width={4200} height={80} fill="#C4A074" />
				<rect x={-1500} y={1095} width={4200} height={110} fill="#DBCEC3" />
				<rect x={-1500} y={1095} width={4200} height={10} fill="#C9B9A9" />
				<rect x={-1500} y={1200} width={4200} height={1800} fill="#C4A074" />
				<Streaks items={DIRT} c="#CDAC82" />
				{/* front hut */}
				<Quonset x={525} y={850} w={640} h={470} c="#69654C" rim="#ABA479" dark="#3E3C2C" door="#333332" strut="#53533D" doorW={210} />
				<rect x={170} y={838} width={710} height={16} rx={8} fill="#000" opacity={0.12} />
				{/* characters */}
				<Soldier
					look={LOOKS.B}
					x={BX}
					y={FY}
					pose={{
						facing: 1,
						mouth: bMouth,
						brows: t > 11.3 ? 'happy' : 'angry',
						eyes: blinking(t, 2) ? 'closed' : 'open',
						breathe: t * 0.4,
						handF: t < 9 ? bPoint : 'side',
						pointF: t < 9,
						headRot: t > 11.3 ? nod - 2 : Math.sin(t * 5) * (bTalking ? 2 : 0.5),
						lookX: t > 11.3 ? 2.5 : 2,
					}}
				/>
				<Soldier
					look={LOOKS.A}
					x={AX}
					y={FY}
					pose={{
						facing: -1,
						gun: g,
						handN: 'grip',
						handF: 'fore',
						mouth: aMouth,
						brows: 'angry',
						eyes: blinking(t, 5) ? 'closed' : 'open',
						breathe: t * 0.4 + 0.3,
						headY: aTalk ? Math.sin(t * 9) * 3 : 0,
						headRot: aTalk ? Math.sin(t * 4.3) * 2 : 0,
						lookX: 1.8,
					}}
				/>
			</g>
			{/* FX in screen space (S06 sparkles on the receiver) */}
			<Sparkle t={t} t0={9.25} x={560} y={640} size={300} />
			<Sparkle t={t} t0={9.5} x={430} y={520} size={450} dur={0.55} />
			<Sparkle t={t} t0={9.62} x={600} y={720} size={120} />
			{/* UI: calendar pinned to the screen 7.25-14.25 */}
			{t >= 7.25 && <CalendarUI t={t} />}
			{/* UI: clipboard 11.35+ */}
			{t >= 11.35 && <ClipboardUI t={t} />}
		</g>
	);
};

const CalendarUI: React.FC<{t: number}> = ({t}) => {
	const u = clamp((t - 7.25) / 0.3);
	const sc = u < 0.6 ? E.outCubic(u / 0.6) * 1.1 : 1.1 - 0.1 * E.inOutCubic((u - 0.6) / 0.4);
	const digits = t >= 8.97 ? '2023' : t >= 8.8 ? '202' : t >= 8.63 ? '20' : t >= 8.47 ? '2' : '';
	return (
		<g transform={`translate(270 240) scale(${sc * 1.2}) translate(-110 -98)`}>
			<Calendar text={digits} />
		</g>
	);
};

const ClipboardUI: React.FC<{t: number}> = ({t}) => {
	const u = clamp((t - 11.35) / 0.4);
	const e = E.outBack(u);
	const rot = 30 + (5 - 30) * e;
	const dy = (1 - E.outCubic(u)) * 900;
	const sway = Math.sin(t * 2.2) * 1.2;
	return (
		<g transform={`translate(640 ${1130 + dy}) rotate(${rot + sway}) scale(1.5) translate(-170 -470)`}>
			<Clipboard t={t} checks={[12.25, 12.75, 13.25]} />
		</g>
	);
};
