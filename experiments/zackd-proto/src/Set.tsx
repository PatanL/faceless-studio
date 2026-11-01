// One set: a walk-in freezer (rigid, code-friendly) plus the warm room seen through the door.
// Palette from VISUAL_GRAMMAR 4.2: pale powder/cyan-blue walls, steel-blue floor, warm tan cardboard,
// signal colours only with meaning (green = named/glowing thing, yellow = input highlight).
import React, {useMemo} from 'react';
import {AdditiveBlending, BackSide} from 'three';
import {doorAngle, knobGlow, knobPush, latchHighlight} from './timeline';
import {useRadialTexture} from './fx';

export const ROOM = {x0: -1.6, x1: 1.6, h: 2.6, z0: -2.0, z1: 3.0};
const DOOR = {x0: -0.2, x1: 0.8, h: 2.04};

const C = {
	wall: '#8fc0de',
	seam: '#5d86a8',
	ceiling: '#b9dcef',
	floor: '#5f84a3',
	trim: '#3b5677',
	steel: '#b9cddc',
	doorFace: '#a8c9de',
	card: '#ceb28a',
	cardDark: '#9f7547',
	tub: '#eef5f8',
	crate: '#2f74b5',
	frost: '#eef9ff',
	ice: '#dff4ff',
	warmWall: '#ffd59c',
	warmFloor: '#c4915e',
	knob: '#d9ead0',
	green: '#2edb31',
	greenHalo: '#57bf44',
	yellow: '#e3c671',
};

type BoxP = {p: [number, number, number]; s: [number, number, number]; c: string; r?: number; m?: number; cast?: boolean; recv?: boolean};
const Box: React.FC<BoxP> = ({p, s, c, r = 0.6, m = 0, cast = false, recv = true}) => (
	<mesh position={p} castShadow={cast} receiveShadow={recv}>
		<boxGeometry args={s} />
		<meshStandardMaterial color={c} roughness={r} metalness={m} />
	</mesh>
);

// deterministic pseudo-random
const rnd = (i: number) => {
	const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
	return x - Math.floor(x);
};

const Rack: React.FC<{x: number; z0: number; z1: number; seed: number; face: 1 | -1}> = ({x, z0, z1, seed, face}) => {
	const items = useMemo(() => {
		const out: React.ReactNode[] = [];
		const levels = [0.36, 0.96, 1.56];
		levels.forEach((y, li) => {
			let z = z0 + 0.05;
			let i = 0;
			while (z < z1 - 0.2) {
				const k = seed * 100 + li * 20 + i;
				const kind = rnd(k) < 0.55 ? 'card' : rnd(k) < 0.8 ? 'tub' : 'crate';
				const w = kind === 'tub' ? 0.24 : 0.28 + 0.12 * rnd(k + 1);
				const h = kind === 'tub' ? 0.2 : 0.18 + 0.2 * rnd(k + 2);
				const d = 0.42;
				const cz = z + w / 2;
				const cx = x + face * 0.02 * (rnd(k + 3) - 0.5);
				if (kind === 'tub') {
					out.push(
						<mesh key={k} position={[cx, y + 0.013 + h / 2, cz]} castShadow receiveShadow>
							<cylinderGeometry args={[0.11, 0.1, h, 14]} />
							<meshStandardMaterial color={C.tub} roughness={0.25} />
						</mesh>,
					);
				} else {
					out.push(<Box key={k} p={[cx, y + 0.013 + h / 2, cz]} s={[d, h, w]} c={kind === 'card' ? C.card : C.crate} r={kind === 'card' ? 0.8 : 0.4} cast />);
					// cardboard tape stripe
					if (kind === 'card') out.push(<Box key={`${k}t`} p={[cx, y + 0.013 + h + 0.001, cz]} s={[d + 0.002, 0.004, 0.05]} c={C.cardDark} r={0.5} />);
				}
				// frost cap
				out.push(<Box key={`${k}f`} p={[cx, y + 0.013 + h + 0.008, cz]} s={[d * 0.9, 0.014, w * 0.85]} c={C.frost} r={0.95} />);
				z += w + 0.05 + 0.06 * rnd(k + 4);
				i++;
			}
		});
		return out;
	}, [x, z0, z1, seed, face]);
	const len = z1 - z0;
	return (
		<group>
			{[0.36, 0.96, 1.56, 2.1].map((y) => (
				<Box key={y} p={[x, y, (z0 + z1) / 2]} s={[0.5, 0.025, len]} c={C.steel} r={0.35} m={0.6} cast />
			))}
			{[z0, z1].flatMap((z) =>
				[x - 0.23, x + 0.23].map((px) => (
					<mesh key={`${z}${px}`} position={[px, 1.1, z]} castShadow>
						<cylinderGeometry args={[0.016, 0.016, 2.2, 8]} />
						<meshStandardMaterial color={C.steel} roughness={0.3} metalness={0.7} />
					</mesh>
				)),
			)}
			{items}
		</group>
	);
};

const Icicles: React.FC = () => {
	const list = useMemo(() => {
		const out: {p: [number, number, number]; l: number; r: number}[] = [];
		for (let i = 0; i < 46; i++) {
			const side = i % 3;
			const u = rnd(i + 900);
			const l = 0.05 + 0.16 * rnd(i + 950);
			const p: [number, number, number] =
				side === 0 ? [ROOM.x0 + 0.03, ROOM.h - l / 2, ROOM.z0 + 0.2 + u * 4.6] : side === 1 ? [ROOM.x1 - 0.03, ROOM.h - l / 2, ROOM.z0 + 0.3 + u * 4.5] : [ROOM.x0 + 0.2 + u * 2.9, ROOM.h - l / 2, ROOM.z0 + 0.08];
			if (side === 2 && p[0] > DOOR.x0 - 0.05 && p[0] < DOOR.x1 + 0.05) p[1] = ROOM.h - 0.53 - l / 2; // over the door frame
			out.push({p, l, r: 0.012 + 0.012 * rnd(i + 990)});
		}
		return out;
	}, []);
	return (
		<group>
			{list.map((ic, i) => (
				<mesh key={i} position={ic.p} rotation={[Math.PI, 0, 0]}>
					<coneGeometry args={[ic.r, ic.l, 6]} />
					<meshStandardMaterial color={C.ice} roughness={0.12} metalness={0.1} transparent opacity={0.85} />
				</mesh>
			))}
		</group>
	);
};

/** panel wall with seams, lying in a plane; axis 'x' = wall normal along x */
const PanelWall: React.FC<{axis: 'x' | 'z'; at: number; from: number; to: number; inward: 1 | -1}> = ({axis, at, from, to, inward}) => {
	const len = to - from;
	const mid = (from + to) / 2;
	const seams: number[] = [];
	for (let u = from + 0.6; u < to - 0.05; u += 0.6) seams.push(u);
	return (
		<group>
			{axis === 'x' ? (
				<Box p={[at, ROOM.h / 2, mid]} s={[0.1, ROOM.h, len]} c={C.wall} r={0.5} m={0.15} />
			) : (
				<Box p={[mid, ROOM.h / 2, at]} s={[len, ROOM.h, 0.1]} c={C.wall} r={0.5} m={0.15} />
			)}
			{seams.map((u) =>
				axis === 'x' ? (
					<Box key={u} p={[at + inward * 0.052, ROOM.h / 2, u]} s={[0.006, ROOM.h, 0.018]} c={C.seam} />
				) : (
					<Box key={u} p={[u, ROOM.h / 2, at + inward * 0.052]} s={[0.018, ROOM.h, 0.006]} c={C.seam} />
				),
			)}
		</group>
	);
};

export const Door: React.FC<{t: number}> = ({t}) => {
	const tex = useRadialTexture();
	const ang = doorAngle(t);
	const glow = knobGlow(t);
	const hi = latchHighlight(t);
	const push = knobPush(t);
	const w = DOOR.x1 - DOOR.x0 - 0.05;
	return (
		<group position={[DOOR.x0 + 0.025, 0, ROOM.z0]} rotation={[0, ang, 0]}>
			{/* slab */}
			<Box p={[w / 2, 1.0, 0]} s={[w, 1.98, 0.1]} c={C.doorFace} r={0.4} m={0.35} cast />
			{/* inner face embossed panel + frost along the bottom */}
			<Box p={[w / 2, 1.05, 0.052]} s={[w - 0.16, 1.6, 0.008]} c="#b8d6e8" r={0.35} m={0.4} />
			<Box p={[w / 2, 0.08, 0.055]} s={[w - 0.04, 0.09, 0.012]} c={C.frost} r={0.95} />
			<Box p={[w / 2, 1.95, 0.055]} s={[w - 0.04, 0.05, 0.012]} c={C.frost} r={0.95} />
			{/* latch housing on the free edge */}
			<group position={[w - 0.11, 1.05, 0.085]}>
				<Box p={[0, 0, 0]} s={[0.1, 0.24, 0.06]} c="#8aa3b8" r={0.3} m={0.7} cast />
				<Box p={[0.035, 0, 0.032]} s={[0.03, 0.18, 0.012]} c="#5b7189" r={0.3} m={0.7} />
				{hi > 0.01 && (
					<mesh scale={[1.25, 1.12, 1.3]}>
						<boxGeometry args={[0.1, 0.24, 0.06]} />
						<meshBasicMaterial color={C.yellow} side={BackSide} transparent opacity={hi} />
					</mesh>
				)}
			</group>
			{/* safety release: rod through the door + mushroom knob */}
			<group position={[w - 0.27, 1.02, 0.05 - 0.022 * push]}>
				<mesh position={[0, 0, 0.04]} rotation={[Math.PI / 2, 0, 0]}>
					<cylinderGeometry args={[0.013, 0.013, 0.08, 10]} />
					<meshStandardMaterial color="#9fb2c2" roughness={0.3} metalness={0.8} />
				</mesh>
				<mesh position={[0, 0, 0.085]} scale={[1, 1, 0.62]} castShadow>
					<sphereGeometry args={[0.046, 22, 14]} />
					<meshStandardMaterial color={C.knob} roughness={0.25} emissive={C.green} emissiveIntensity={1.1 * glow} />
				</mesh>
				{glow > 0.01 && (
					<>
						<mesh position={[0, 0, 0.085]} scale={[1.14, 1.14, 0.62 * 1.2]}>
							<sphereGeometry args={[0.046, 18, 12]} />
							<meshBasicMaterial color={C.green} side={BackSide} transparent opacity={0.95 * glow} />
						</mesh>
						<sprite position={[0, 0, 0.11]} scale={[0.22, 0.22, 1]}>
							<spriteMaterial map={tex} color={C.greenHalo} transparent opacity={0.6 * glow} blending={AdditiveBlending} depthWrite={false} />
						</sprite>
					</>
				)}
				<pointLight position={[0, 0, 0.2]} color={C.green} intensity={0.12 * glow} distance={0.6} decay={2} />
			</group>
		</group>
	);
};

export const Set: React.FC<{t: number; room: number}> = ({t, room}) => (
	<group>
		{/* floor + ceiling */}
		<Box p={[0, -0.05, (ROOM.z0 + ROOM.z1) / 2]} s={[3.3, 0.1, ROOM.z1 - ROOM.z0]} c={C.floor} r={0.38} m={0.35} />
		{Array.from({length: 9}, (_, i) => (
			<Box key={i} p={[0, 0.002, ROOM.z0 + 0.5 + i * 0.55]} s={[3.2, 0.004, 0.012]} c="#4d6e8d" r={0.4} />
		))}
		<mesh position={[0, ROOM.h + 0.05, (ROOM.z0 + ROOM.z1) / 2]}>
			<boxGeometry args={[3.3, 0.1, ROOM.z1 - ROOM.z0]} />
			<meshStandardMaterial color={C.ceiling} roughness={0.6} emissive="#6c9cc4" emissiveIntensity={0.55 * room} />
		</mesh>
		{/* walls */}
		<PanelWall axis="x" at={ROOM.x0 - 0.05} from={ROOM.z0} to={ROOM.z1} inward={1} />
		<PanelWall axis="x" at={ROOM.x1 + 0.05} from={ROOM.z0} to={ROOM.z1} inward={-1} />
		<PanelWall axis="z" at={ROOM.z1 + 0.05} from={ROOM.x0} to={ROOM.x1} inward={-1} />
		{/* back wall with the doorway */}
		<Box p={[(ROOM.x0 + DOOR.x0) / 2, ROOM.h / 2, ROOM.z0]} s={[DOOR.x0 - ROOM.x0, ROOM.h, 0.12]} c={C.wall} r={0.5} m={0.15} />
		<Box p={[(DOOR.x1 + ROOM.x1) / 2, ROOM.h / 2, ROOM.z0]} s={[ROOM.x1 - DOOR.x1, ROOM.h, 0.12]} c={C.wall} r={0.5} m={0.15} />
		<Box p={[(DOOR.x0 + DOOR.x1) / 2, (DOOR.h + ROOM.h) / 2, ROOM.z0]} s={[DOOR.x1 - DOOR.x0, ROOM.h - DOOR.h, 0.12]} c={C.wall} r={0.5} m={0.15} />
		{[-1.0, -0.6].map((x) => (
			<Box key={x} p={[x, ROOM.h / 2, ROOM.z0 + 0.062]} s={[0.018, ROOM.h, 0.006]} c={C.seam} />
		))}
		{/* door frame trim + frost on the gasket */}
		<Box p={[DOOR.x0 - 0.035, DOOR.h / 2, ROOM.z0 + 0.07]} s={[0.07, DOOR.h + 0.07, 0.03]} c={C.trim} r={0.4} m={0.5} />
		<Box p={[DOOR.x1 + 0.035, DOOR.h / 2, ROOM.z0 + 0.07]} s={[0.07, DOOR.h + 0.07, 0.03]} c={C.trim} r={0.4} m={0.5} />
		<Box p={[(DOOR.x0 + DOOR.x1) / 2, DOOR.h + 0.035, ROOM.z0 + 0.07]} s={[DOOR.x1 - DOOR.x0 + 0.14, 0.07, 0.03]} c={C.trim} r={0.4} m={0.5} />
		<Box p={[(DOOR.x0 + DOOR.x1) / 2, DOOR.h + 0.075, ROOM.z0 + 0.08]} s={[DOOR.x1 - DOOR.x0 + 0.14, 0.018, 0.03]} c={C.frost} r={0.95} />
		<Door t={t} />
		{/* wall thermometer prop (in-world, no text) */}
		<group position={[-0.75, 1.62, ROOM.z0 + 0.075]}>
			<mesh rotation={[Math.PI / 2, 0, 0]}>
				<cylinderGeometry args={[0.1, 0.1, 0.03, 24]} />
				<meshStandardMaterial color="#f4f7f9" roughness={0.3} />
			</mesh>
			<mesh position={[0, 0, 0.017]} rotation={[0, 0, -2.2]}>
				<boxGeometry args={[0.008, 0.08, 0.004]} />
				<meshBasicMaterial color="#2c7be5" />
			</mesh>
		</group>
		{/* ceiling lamp (emissive, follows room dimming) */}
		<group position={[0.0, ROOM.h - 0.04, 0.45]}>
			<Box p={[0, 0, 0]} s={[1.0, 0.05, 0.22]} c="#d7e6ef" r={0.4} m={0.4} />
			<mesh position={[0, -0.035, 0]}>
				<boxGeometry args={[0.9, 0.025, 0.14]} />
				<meshBasicMaterial color={`rgb(${Math.round(150 + 105 * room)},${Math.round(170 + 85 * room)},${Math.round(185 + 70 * room)})`} />
			</mesh>
		</group>
		{/* racks */}
		<Rack x={ROOM.x0 + 0.3} z0={-1.3} z1={2.8} seed={1} face={1} />
		<Rack x={ROOM.x1 - 0.3} z0={0.25} z1={2.8} seed={2} face={-1} />
		<Icicles />
		{/* frost drifts in the floor corners */}
		{[
			[ROOM.x0 + 0.08, ROOM.z0 + 0.1],
			[ROOM.x1 - 0.08, ROOM.z0 + 0.1],
			[ROOM.x0 + 0.06, 1.2],
			[ROOM.x1 - 0.06, -0.4],
		].map(([x, z], i) => (
			<mesh key={i} position={[x, 0.0, z]} scale={[0.35, 0.09, 0.6]}>
				<sphereGeometry args={[1, 14, 8, 0, Math.PI * 2, 0, Math.PI / 2]} />
				<meshStandardMaterial color={C.frost} roughness={0.95} />
			</mesh>
		))}
		{/* the warm room outside the door (unlit, always bright) */}
		<mesh position={[0.3, 1.3, ROOM.z0 - 2.6]}>
			<planeGeometry args={[6, 3.2]} />
			<meshBasicMaterial color={C.warmWall} />
		</mesh>
		<mesh position={[-1.4, 1.3, ROOM.z0 - 1.3]} rotation={[0, Math.PI / 2, 0]}>
			<planeGeometry args={[2.6, 3.2]} />
			<meshBasicMaterial color="#f5c486" />
		</mesh>
		<mesh position={[2.0, 1.3, ROOM.z0 - 1.3]} rotation={[0, -Math.PI / 2, 0]}>
			<planeGeometry args={[2.6, 3.2]} />
			<meshBasicMaterial color="#f5c486" />
		</mesh>
		<mesh position={[0.3, 0.0, ROOM.z0 - 1.3]} rotation={[-Math.PI / 2, 0, 0]}>
			<planeGeometry args={[4, 2.6]} />
			<meshBasicMaterial color={C.warmFloor} />
		</mesh>
	</group>
);
