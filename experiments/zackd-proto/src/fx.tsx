// Literalized icons and atmosphere: frost motes, breath puffs, body-heat aura (heat ramp orange -> cyan).
import React, {useMemo} from 'react';
import {AdditiveBlending, BufferAttribute, BufferGeometry, CanvasTexture, Color, SRGBColorSpace} from 'three';
import {CharPose, mouthWorld} from './Character';
import {V3, clamp, lerp} from './timeline';

let RADIAL: CanvasTexture | null = null;
/** soft white radial gradient (shared) for glows, puffs and motes */
export function useRadialTexture() {
	return useMemo(() => {
		if (RADIAL) return RADIAL;
		const c = document.createElement('canvas');
		c.width = c.height = 128;
		const g = c.getContext('2d')!;
		const grad = g.createRadialGradient(64, 64, 0, 64, 64, 64);
		grad.addColorStop(0, 'rgba(255,255,255,1)');
		grad.addColorStop(0.35, 'rgba(255,255,255,0.6)');
		grad.addColorStop(1, 'rgba(255,255,255,0)');
		g.fillStyle = grad;
		g.fillRect(0, 0, 128, 128);
		RADIAL = new CanvasTexture(c);
		RADIAL.colorSpace = SRGBColorSpace;
		return RADIAL;
	}, []);
}

const rnd = (i: number) => {
	const x = Math.sin(i * 91.7 + 17.3) * 43758.5453;
	return x - Math.floor(x);
};

/** floating ice crystals filling the room, slowly falling (deterministic in t) */
export const FrostMotes: React.FC<{t: number; n?: number}> = ({t, n = 420}) => {
	const tex = useRadialTexture();
	const geo = useMemo(() => {
		const g = new BufferGeometry();
		g.setAttribute('position', new BufferAttribute(new Float32Array(n * 3), 3));
		return g;
	}, [n]);
	const arr = geo.getAttribute('position').array as Float32Array;
	for (let i = 0; i < n; i++) {
		const y0 = rnd(i * 3 + 1) * 2.6;
		const y = ((y0 - 0.08 * t) % 2.6 + 2.6) % 2.6;
		arr[i * 3] = -1.55 + rnd(i * 3) * 3.1 + 0.03 * Math.sin(t * 0.9 + i);
		arr[i * 3 + 1] = y;
		arr[i * 3 + 2] = -1.95 + rnd(i * 3 + 2) * 4.9;
	}
	geo.getAttribute('position').needsUpdate = true;
	return (
		<points geometry={geo}>
			<pointsMaterial map={tex} size={0.022} sizeAttenuation transparent opacity={0.85} color="#f2fbff" depthWrite={false} />
		</points>
	);
};

/** breath vapour: a puff every 1.05 s from the mouth, drifting forward and up */
export const Breath: React.FC<{t: number; pose: CharPose; on: boolean}> = ({t, pose, on}) => {
	const tex = useRadialTexture();
	if (!on) return null;
	const m = mouthWorld(pose);
	const fwd: V3 = [Math.sin(pose.yaw), 0, Math.cos(pose.yaw)];
	const puffs: React.ReactNode[] = [];
	const period = 1.05;
	for (let k = -1; k <= 1; k++) {
		const tb = Math.floor(t / period) * period + k * period;
		const a = (t - tb) / 0.95;
		if (a < 0 || a > 1) continue;
		const d = 0.05 + 0.32 * a;
		const s = 0.07 + 0.32 * a;
		puffs.push(
			<sprite key={tb.toFixed(2)} position={[m[0] + fwd[0] * d, m[1] - 0.02 + 0.1 * a, m[2] + fwd[2] * d]} scale={[s, s * 0.8, 1]}>
				<spriteMaterial map={tex} color="#ffffff" transparent opacity={0.55 * (1 - a) * Math.min(1, a * 6)} depthWrite={false} />
			</sprite>,
		);
	}
	return <group>{puffs}</group>;
};

const WARM = new Color('#ff9a1f');
const HOT = new Color('#e5322b');
const COLD = new Color('#38d4eb');

/** body heat: orange aura behind the figure + wisps that leave the body and cool to cyan */
export const HeatAura: React.FC<{t: number; pose: CharPose; level: number; on: boolean}> = ({t, pose, level, on}) => {
	const tex = useRadialTexture();
	if (!on) return null;
	const [px, , pz] = pose.pos;
	const wisps: React.ReactNode[] = [];
	const n = 26;
	for (let i = 0; i < n; i++) {
		const life = (t * (0.55 + 0.25 * rnd(i)) + rnd(i + 40)) % 1;
		const ang = rnd(i + 80) * Math.PI * 2;
		const r = 0.22 + 0.55 * life;
		const y = 0.55 + rnd(i + 120) * 1.0 + 0.45 * life;
		const col = WARM.clone().lerp(COLD, clamp(life * 1.3));
		const s = lerp(0.2, 0.08, life);
		wisps.push(
			<sprite key={i} position={[px + Math.cos(ang) * r, y, pz + Math.sin(ang) * r * 0.8]} scale={[s, s, 1]}>
				<spriteMaterial map={tex} color={col} transparent opacity={0.9 * level * (1 - life)} depthWrite={false} blending={AdditiveBlending} />
			</sprite>,
		);
	}
	const auraCol = HOT.clone().lerp(WARM, 0.55 + 0.45 * level);
	const sc = 1.6 + 0.9 * level;
	return (
		<group>
			<sprite position={[px, 1.05, pz]} scale={[sc * 0.85, sc * 1.25, 1]} renderOrder={-1}>
				<spriteMaterial map={tex} color={auraCol} transparent opacity={0.9 * level} depthWrite={false} depthTest={false} />
			</sprite>
			{wisps}
		</group>
	);
};
