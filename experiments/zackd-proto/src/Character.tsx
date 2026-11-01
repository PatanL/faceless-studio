// One stylised low-poly person (1:5.7 heads, head 1.15x, hands 1.2x), one flat wardrobe colour (orange hoodie)
// so the warm subject pops against the cobalt/cyan freezer. All pose and expression values are functions of t.
import React from 'react';
import {Euler} from 'three';
import {KNOCKS, SLAM, V3, W, clamp, easeInOut, easeOut, lerp, ramp} from './timeline';

export const COL = {
	hoodie: '#f47a35',
	hoodieDark: '#c95a22',
	pants: '#26355e',
	shoe: '#1b2238',
	skin: '#e3a27e',
	hair: '#3b2618',
	eye: '#f4f3f0',
	pupil: '#10182c',
	mouth: '#5a1e2a',
	frost: '#e4f6ff',
};

type Arm = {x: number; y: number; z: number; elbow: number};
type Expr = {browUp: number; browTilt: number; mouthOpen: number; mouthWide: number; teeth: number; eyesClosed: number};

const REST_A: Arm = {x: 0.05, y: 0, z: 0.12, elbow: -0.15};
const HUG_A: Arm = {x: -0.55, y: -0.95, z: 0.25, elbow: -2.0};
const RAISED_A: Arm = {x: -2.55, y: -0.15, z: 0.1, elbow: -1.0};
const STRIKE_A: Arm = {x: -1.6, y: -0.1, z: 0.05, elbow: -0.12};
const TIRED_A: Arm = {x: -1.25, y: -0.15, z: 0.05, elbow: -0.35};
const mirror = (a: Arm): Arm => ({x: a.x, y: -a.y, z: -a.z, elbow: a.elbow});
const mixArm = (a: Arm, b: Arm, k: number): Arm => ({
	x: lerp(a.x, b.x, k),
	y: lerp(a.y, b.y, k),
	z: lerp(a.z, b.z, k),
	elbow: lerp(a.elbow, b.elbow, k),
});

const NEUTRAL: Expr = {browUp: 0, browTilt: 0, mouthOpen: 0.15, mouthWide: 1, teeth: 0, eyesClosed: 0};
const SHOCK: Expr = {browUp: 0.022, browTilt: 0.25, mouthOpen: 1, mouthWide: 0.8, teeth: 0, eyesClosed: 0};
const COLD: Expr = {browUp: 0.012, browTilt: 0.4, mouthOpen: 0.35, mouthWide: 1.5, teeth: 1, eyesClosed: 0};
const EFFORT: Expr = {browUp: -0.01, browTilt: -0.45, mouthOpen: 0.75, mouthWide: 1.5, teeth: 1, eyesClosed: 0.3};
const RELIEF: Expr = {browUp: 0.006, browTilt: 0.15, mouthOpen: 0.1, mouthWide: 1.3, teeth: 0, eyesClosed: 1};
const mixExpr = (a: Expr, b: Expr, k: number): Expr => {
	const o = {} as Expr;
	(Object.keys(a) as (keyof Expr)[]).forEach((key) => (o[key] = lerp(a[key], b[key], k)));
	return o;
};

/** strike level 0..1 for one fist: comes down onto the door at each of its knock times */
const strike = (t: number, times: number[]) =>
	Math.max(0, ...times.map((k) => (t < k ? easeInOut(ramp(t, k - 0.13, k)) : 1 - easeInOut(ramp(t, k + 0.02, k + 0.2)))));

export type CharPose = {
	pos: V3;
	yaw: number;
	armA: Arm; // character's left (+x local)
	armB: Arm;
	expr: Expr;
	shiver: number;
	frost: number;
	shrug: number;
};

export function charPose(t: number): CharPose {
	const base: V3 = [0.3, 0, -0.8];
	if (t < 1.36) {
		const flinch = clamp(1 - Math.abs(t - SLAM - 0.08) / 0.25);
		return {
			pos: base,
			yaw: Math.PI - 0.75 * (1 - easeOut(ramp(t, 0, 0.55))),
			armA: mixArm(REST_A, {...REST_A, x: -0.5, elbow: -1.2}, flinch),
			armB: mirror(mixArm(REST_A, {...REST_A, x: -0.5, elbow: -1.2}, flinch)),
			expr: mixExpr(NEUTRAL, SHOCK, easeOut(ramp(t, SLAM - 0.05, SLAM + 0.15))),
			shiver: 0,
			frost: 0,
			shrug: flinch,
		};
	}
	if (t < W.freezer) {
		return {
			pos: base,
			yaw: lerp(Math.PI, 0.35, easeInOut(ramp(t, 1.36, 2.3))),
			armA: mixArm(REST_A, HUG_A, easeInOut(ramp(t, 1.8, 2.38))),
			armB: mirror(mixArm(REST_A, HUG_A, easeInOut(ramp(t, 1.8, 2.38)))),
			expr: mixExpr(SHOCK, COLD, ramp(t, 1.6, 2.3)),
			shiver: ramp(t, 1.8, 2.38),
			frost: 0.3,
			shrug: 0.5,
		};
	}
	if (t < W.pounding) {
		return {
			pos: base,
			yaw: 0.12,
			armA: HUG_A,
			armB: mirror(HUG_A),
			expr: COLD,
			shiver: 1,
			frost: lerp(0.5, 1, ramp(t, 2.38, 4.5)),
			shrug: 0.7,
		};
	}
	if (t < W.because) {
		const tired = easeInOut(ramp(t, 5.75, 6.5));
		const a = mixArm(mixArm(RAISED_A, STRIKE_A, strike(t, [KNOCKS[0], KNOCKS[2]])), TIRED_A, tired);
		const b = mixArm(mixArm(RAISED_A, STRIKE_A, strike(t, [KNOCKS[1]])), TIRED_A, tired);
		return {
			pos: [0.3, 0, -1.36],
			yaw: Math.PI,
			armA: a,
			armB: mirror(b),
			expr: EFFORT,
			shiver: 0.3,
			frost: 1,
			shrug: 0.2,
		};
	}
	// payoff wide (same pose as frame 0 at the very end, for the loop)
	const k = easeInOut(ramp(t, W.open, W.open + 0.8));
	return {
		pos: base,
		yaw: Math.PI,
		armA: REST_A,
		armB: mirror(REST_A),
		expr: mixExpr(NEUTRAL, RELIEF, k * (1 - ramp(t, 12.4, 12.9))),
		shiver: 0,
		frost: 1 - ramp(t, 12.0, 12.9),
		shrug: 0,
	};
}

/** world position of the mouth (for breath puffs) */
export function mouthWorld(p: CharPose): V3 {
	const lx = 0;
	const lz = 0.17;
	const s = Math.sin(p.yaw);
	const c = Math.cos(p.yaw);
	return [p.pos[0] + lx * c + lz * s, p.pos[1] + 1.5, p.pos[2] - lx * s + lz * c];
}

const Std: React.FC<{c: string; r?: number; m?: number}> = ({c, r = 0.55, m = 0}) => (
	<meshStandardMaterial color={c} roughness={r} metalness={m} />
);

const ArmView: React.FC<{side: 1 | -1; a: Arm; shrug: number}> = ({side, a, shrug}) => (
	<group position={[side * 0.235, 1.33 + 0.03 * shrug, 0]} rotation={new Euler(a.x, a.y, a.z, 'XYZ')}>
		<mesh position={[0, -0.14, 0]} castShadow>
			<capsuleGeometry args={[0.062, 0.2, 4, 10]} />
			<Std c={COL.hoodie} />
		</mesh>
		<group position={[0, -0.28, 0]} rotation={[a.elbow, 0, 0]}>
			<mesh position={[0, -0.12, 0]} castShadow>
				<capsuleGeometry args={[0.055, 0.18, 4, 10]} />
				<Std c={COL.hoodie} />
			</mesh>
			<mesh position={[0, -0.235, 0]} castShadow>
				<cylinderGeometry args={[0.058, 0.058, 0.04, 12]} />
				<Std c={COL.hoodieDark} />
			</mesh>
			{/* hand 1.2x */}
			<mesh position={[0, -0.3, 0.005]} scale={[1, 1.1, 0.85]} castShadow>
				<sphereGeometry args={[0.06, 14, 10]} />
				<Std c={COL.skin} r={0.5} />
			</mesh>
		</group>
	</group>
);

export const Character: React.FC<{t: number}> = ({t}) => {
	const p = charPose(t);
	const e = p.expr;
	// shiver: small fast deterministic jitter
	const sh = p.shiver * 0.02;
	const jx = sh * Math.sin(t * 61.0);
	const jz = sh * 0.6 * Math.sin(t * 47.0 + 1.3);
	const browCol = lerpColor(COL.hair, COL.frost, 0.75 * p.frost);
	return (
		<group position={p.pos} rotation={[0, p.yaw, 0]}>
			<group position={[jx * 0.3, 0, 0]} rotation={[0, 0, jz]}>
				{/* legs + shoes */}
				{[-1, 1].map((s) => (
					<group key={s}>
						<mesh position={[s * 0.1, 0.44, 0]} castShadow>
							<capsuleGeometry args={[0.085, 0.62, 4, 10]} />
							<Std c={COL.pants} r={0.7} />
						</mesh>
						<mesh position={[s * 0.1, 0.045, 0.04]} scale={[1, 0.7, 1.6]} castShadow>
							<sphereGeometry args={[0.075, 12, 8]} />
							<Std c={COL.shoe} r={0.45} />
						</mesh>
					</group>
				))}
				{/* hoodie torso */}
				<mesh position={[0, 1.12, 0]} scale={[1.12, 1, 0.78]} castShadow>
					<capsuleGeometry args={[0.2, 0.34, 6, 16]} />
					<Std c={COL.hoodie} r={0.62} />
				</mesh>
				{/* front pocket + drawstrings */}
				<mesh position={[0, 0.98, 0.15]} scale={[1, 0.55, 0.25]}>
					<sphereGeometry args={[0.15, 14, 8]} />
					<Std c={COL.hoodieDark} r={0.7} />
				</mesh>
				{[-0.05, 0.05].map((x) => (
					<mesh key={x} position={[x, 1.25, 0.165]}>
						<cylinderGeometry args={[0.007, 0.007, 0.13, 6]} />
						<Std c="#f4f3f0" />
					</mesh>
				))}
				{/* hood collar */}
				<mesh position={[0, 1.38 + 0.03 * p.shrug, -0.03]} rotation={[Math.PI / 2 - 0.15, 0, 0]} castShadow>
					<torusGeometry args={[0.12, 0.055, 8, 18]} />
					<Std c={COL.hoodieDark} r={0.65} />
				</mesh>
				<ArmView side={1} a={p.armA} shrug={p.shrug} />
				<ArmView side={-1} a={p.armB} shrug={p.shrug} />
				{/* head */}
				<group position={[0, 1.56 - 0.02 * p.shrug, 0.01]} rotation={[0.05 + jz * 0.5, 0, jx * 2]}>
					<mesh scale={[0.95, 1.08, 1]} castShadow>
						<sphereGeometry args={[0.145, 20, 16]} />
						<Std c={COL.skin} r={0.5} />
					</mesh>
					{/* hair cap */}
					<mesh position={[0, 0.02, -0.012]} rotation={[-0.35, 0, 0]} scale={[1.0, 1.08, 1.04]}>
						<sphereGeometry args={[0.152, 20, 12, 0, Math.PI * 2, 0, 1.25]} />
						<Std c={COL.hair} r={0.7} />
					</mesh>
					{/* frost on hair */}
					{p.frost > 0.05 && (
						<mesh position={[0, 0.03, -0.012]} rotation={[-0.35, 0, 0]} scale={[1.01, 1.09, 1.05]}>
							<sphereGeometry args={[0.152, 20, 8, 0, Math.PI * 2, 0, 0.55]} />
							<meshStandardMaterial color={COL.frost} roughness={0.9} transparent opacity={0.35 * p.frost} />
						</mesh>
					)}
					{/* ears + nose */}
					{[-1, 1].map((s) => (
						<mesh key={s} position={[s * 0.138, -0.005, 0]} scale={[0.5, 1, 0.8]}>
							<sphereGeometry args={[0.035, 10, 8]} />
							<Std c={COL.skin} />
						</mesh>
					))}
					<mesh position={[0, -0.01, 0.147]} scale={[1, 0.9, 1]}>
						<sphereGeometry args={[0.024, 10, 8]} />
						<Std c="#e8967a" r={0.4} />
					</mesh>
					{/* eyes 1.2x */}
					{[-1, 1].map((s) => (
						<group key={s} position={[s * 0.052, 0.03, 0.122]} scale={[1, Math.max(0.08, 1 - e.eyesClosed), 1]}>
							<mesh scale={[1, 1.15, 0.7]}>
								<sphereGeometry args={[0.032, 14, 10]} />
								<meshStandardMaterial color={COL.eye} roughness={0.2} />
							</mesh>
							<mesh position={[0, 0, 0.02]} scale={[1, 1.1, 0.5]}>
								<sphereGeometry args={[0.017, 12, 8]} />
								<meshStandardMaterial color={COL.pupil} roughness={0.15} />
							</mesh>
							<mesh position={[0.006, 0.008, 0.029]}>
								<sphereGeometry args={[0.005, 6, 4]} />
								<meshBasicMaterial color="#ffffff" />
							</mesh>
						</group>
					))}
					{/* brows: tilt > 0 = inner ends up (worried), < 0 = inner ends down (effort) */}
					{[-1, 1].map((s) => (
						<mesh
							key={s}
							position={[s * 0.055, 0.082 + e.browUp, 0.13]}
							rotation={[0.2, 0, s * -e.browTilt]}
						>
							<boxGeometry args={[0.058, 0.014, 0.014]} />
							<Std c={browCol} r={0.8} />
						</mesh>
					))}
					{/* mouth */}
					<mesh position={[0, -0.068, 0.128]} scale={[0.03 * e.mouthWide, 0.004 + 0.022 * e.mouthOpen, 0.012]}>
						<sphereGeometry args={[1, 14, 8]} />
						<meshStandardMaterial color={COL.mouth} roughness={0.6} />
					</mesh>
					{e.teeth > 0.5 && (
						<mesh position={[0, -0.066, 0.137]} scale={[0.026 * e.mouthWide, 0.007, 0.005]}>
							<sphereGeometry args={[1, 10, 6]} />
							<meshStandardMaterial color="#fbfbf6" roughness={0.3} />
						</mesh>
					)}
				</group>
			</group>
		</group>
	);
};

function lerpColor(a: string, b: string, k: number) {
	const pa = parseInt(a.slice(1), 16);
	const pb = parseInt(b.slice(1), 16);
	const ch = (sh: number) => Math.round(lerp((pa >> sh) & 255, (pb >> sh) & 255, clamp(k)));
	return `#${((ch(16) << 16) | (ch(8) << 8) | ch(0)).toString(16).padStart(6, '0')}`;
}

/** POV forearm for the knob close-up: sleeve + fist + index finger between two points (Zack's "hands only" convention).
 * `hand` is the wrist; the fingertip sits 0.13 m further along the forearm direction. */
export const PovArm: React.FC<{hand: V3; elbow: V3}> = ({hand, elbow}) => {
	const mid: V3 = [(hand[0] + elbow[0]) / 2, (hand[1] + elbow[1]) / 2, (hand[2] + elbow[2]) / 2];
	const d: V3 = [hand[0] - elbow[0], hand[1] - elbow[1], hand[2] - elbow[2]];
	const len = Math.hypot(...d);
	// orient a +y capsule along d
	const yaw = Math.atan2(d[0], d[2]);
	const pitch = Math.acos(clamp(d[1] / len, -1, 1));
	const rot = new Euler(pitch, yaw, 0, 'YXZ');
	return (
		<group>
			<group position={mid} rotation={rot}>
				<mesh castShadow>
					<capsuleGeometry args={[0.05, len, 4, 12]} />
					<Std c={COL.hoodie} r={0.62} />
				</mesh>
				<mesh position={[0, len / 2 - 0.01, 0]}>
					<cylinderGeometry args={[0.054, 0.054, 0.04, 14]} />
					<Std c={COL.hoodieDark} />
				</mesh>
			</group>
			<group position={hand} rotation={rot}>
				{/* fist */}
				<mesh position={[0, 0.045, 0]} scale={[1.05, 1.1, 0.85]} castShadow>
					<sphereGeometry args={[0.045, 16, 12]} />
					<Std c={COL.skin} r={0.45} />
				</mesh>
				{/* index finger */}
				<mesh position={[0.012, 0.1, 0.012]} castShadow>
					<capsuleGeometry args={[0.013, 0.05, 4, 8]} />
					<Std c={COL.skin} r={0.45} />
				</mesh>
				{/* thumb */}
				<mesh position={[-0.035, 0.05, 0.02]} rotation={[0, 0, 0.5]} scale={[0.7, 1.1, 0.7]}>
					<sphereGeometry args={[0.022, 10, 8]} />
					<Std c={COL.skin} r={0.45} />
				</mesh>
			</group>
		</group>
	);
};

export function povArmAt(t: number): {hand: V3; elbow: V3} {
	// enters from the lower left on "knob", fingertip lands on the knob face on "pushes" and pushes it 2 cm
	const k = easeOut(ramp(t, W.knob - 0.05, W.pushes - 0.05));
	const push = 0.022 * easeOut(ramp(t, W.pushes - 0.05, W.pushes + 0.15)) * (1 - easeInOut(ramp(t, W.open + 0.3, W.open + 0.7)));
	const dir: V3 = [0.21, 0.32, -0.93]; // elbow -> wrist, normalised
	const tip: V3 = [0.505, 1.022, -1.84 - push];
	const contact: V3 = [tip[0] - 0.115 * dir[0], tip[1] - 0.115 * dir[1], tip[2] - 0.115 * dir[2]];
	const start: V3 = [0.25, 0.55, -1.25];
	const hand: V3 = [lerp(start[0], contact[0], k), lerp(start[1], contact[1], k), lerp(start[2], contact[2], k)];
	return {hand, elbow: [hand[0] - 0.36 * dir[0], hand[1] - 0.36 * dir[1], hand[2] - 0.36 * dir[2]]};
}
