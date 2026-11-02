/**
 * Fish rendering: one fish (2-3 tone flat shading: back, body, belly + fins, gill, eye, pattern, highlight
 * stroke), schools (seeded formation, per-fish variation in size, heading, phase and colour drift), far
 * silhouette schools and distant rays. Value separation only: no outlines; fins are a translucent mix.
 */
import React from 'react';
import {c, mixOk, rgba, shadowOf} from '../../../kurz-style/engine/src/lib/color';
import {useLight, useTint} from '../../../kurz-style/engine/src/lib/light';
import {noise1, rand} from '../../../kurz-style/engine/src/lib/rng';
import {fishGeom, raySil, SPECIES, type FishGeom} from './species';
import {schoolPoses, type FishPose, type SchoolSpec} from './schools';

export type {FishPose, SchoolSpec};

const geomCache = new Map<string, FishGeom>();
const geom = (sp: string, seed: string) => {
	const k = `${sp}:${seed}`;
	let g = geomCache.get(k);
	if (!g) {
		g = fishGeom(SPECIES[sp], seed);
		geomCache.set(k, g);
	}
	return g;
};


export const Fish: React.FC<{species: string; seed: string; pose: FishPose; flat?: string}> = ({species, seed, pose, flat}) => {
	const tint = useTint();
	const L = useLight();
	const sp = SPECIES[species];
	const g = geom(species, seed);
	const flipY = Math.cos((pose.ang * Math.PI) / 180) < 0 ? -1 : 1; // heading left -> keep the back up
	const s = pose.len / 100;
	const beat = pose.beat ?? 8;
	const tailA = 16 * Math.sin(pose.t * beat + pose.phase);
	const flex = 0.05 * Math.sin(pose.t * beat + pose.phase - 1);
	const tr = `translate(${pose.x.toFixed(1)} ${pose.y.toFixed(1)}) rotate(${pose.ang.toFixed(1)}) scale(${s.toFixed(3)} ${(s * flipY).toFixed(3)}) skewY(${(flex * 30).toFixed(2)})`;
	if (flat) {
		const col = tint(flat);
		return (
			<g transform={tr}>
				<path d={g.tail} fill={col} transform={`rotate(${tailA.toFixed(1)} -48 0)`} />
				<path d={g.dorsal} fill={col} />
				<path d={g.anal} fill={col} />
				<path d={g.body} fill={col} />
			</g>
		);
	}
	const body = tint(mixOk(c(sp.body), c(sp.alt), g.drift));
	const back = shadowOf(tint(sp.back), tint(L.ambient), 0.12);
	const belly = tint(sp.belly);
	const finCol = mixOk(body, back, 0.45);
	const hiCol = mixOk(body, tint(L.keyColor), 0.35);
	const acc = tint(sp.accent);
	return (
		<g transform={tr}>
			<path d={g.tail} fill={finCol} opacity={0.92} transform={`rotate(${tailA.toFixed(1)} -48 0)`} />
			<path d={g.dorsal} fill={finCol} opacity={0.9} />
			<path d={g.anal} fill={finCol} opacity={0.9} />
			<path d={g.body} fill={body} />
			<path d={g.back} fill={back} />
			<path d={g.belly} fill={belly} opacity={0.9} />
			{g.pattern.map((p, i) =>
				p.stroke ? <path key={i} d={p.d} stroke={acc} strokeWidth={p.stroke} strokeLinecap="round" fill="none" opacity={0.9} /> : <path key={i} d={p.d} fill={acc} opacity={0.85} />,
			)}
			<path d={g.gill} stroke={mixOk(body, back, 0.6)} strokeWidth={2.2 / s > 6 ? 6 : 2.2 / s} fill="none" strokeLinecap="round" />
			<path d={g.pec} fill={mixOk(finCol, belly, 0.3)} opacity={0.8} transform={`rotate(${(8 * Math.sin(pose.t * 5 + pose.phase)).toFixed(1)} ${g.eye[0] - g.eye[2] * 3.2} ${g.eye[1]})`} />
			<path d={g.hiLine} stroke={hiCol} strokeWidth={Math.max(1.4 / s, 2)} fill="none" strokeLinecap="round" opacity={0.75} />
			<circle cx={g.eye[0]} cy={g.eye[1]} r={g.eye[2]} fill={tint('bone-1')} />
			<circle cx={g.eye[0] + g.eye[2] * 0.12} cy={g.eye[1]} r={g.eye[2] * 0.62} fill={tint('ink-1')} />
			<circle cx={g.eye[0] + g.eye[2] * 0.35} cy={g.eye[1] - g.eye[2] * 0.3} r={g.eye[2] * 0.24} fill={c('bone-2')} />
		</g>
	);
};

export const School: React.FC<{spec: SchoolSpec; t: number}> = ({spec, t}) => (
	<g>
		{schoolPoses(spec, t).map((p, i) => (
			<Fish key={i} species={spec.species} seed={`${spec.id}-${i}`} pose={p} flat={spec.flat} />
		))}
	</g>
);

export const Ray: React.FC<{x: number; y: number; s: number; ang: number; t: number; color?: string; seed: string}> = ({x, y, s, ang, t, color = 'ink-4', seed}) => {
	const tint = useTint();
	return (
		<path
			d={raySil(t * 0.28 + rand(seed, 1))}
			fill={tint(color)}
			transform={`translate(${(x + 8 * t).toFixed(1)} ${(y + 4 * noise1(seed, t * 0.3)).toFixed(1)}) rotate(${ang}) scale(${s})`}
		/>
	);
};

/** translucent fin colour helper for other generators */
export const finTone = (a: string, b: string) => rgba(mixOk(a, b, 0.4), 0.85);
