/**
 * 4 s detail-pass showcase (1080x1920, 30 fps): a sunlit reef with a hero sea turtle, built only from the
 * detail generators in src/detail plus the engine's planes, light, atmosphere and <Shaded>.
 *
 *   P0 field    tide gradient + surface band; rays, caustics, sun (ONE screen layer)
 *   P1 far      far reef mounds + scattered coral silhouettes, far kelp, silhouette schools, an eagle ray, micro
 *   P2 mid      back reef scatter (families, edge bias, calm-field rejection), kelp groves, 4 schools, micro
 *   P3 subject  hero turtle (+ surface marks), front reef row, single fish, micro, regulator-free bubbles
 *   P4 fore     cropped kelp + coral silhouettes, bokeh
 * The calm field (CALM, ~35 % of the frame) holds only the hero, the water gradient, rays and the micro layer.
 */
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {c, mixOk, rgba} from '../../../kurz-style/engine/src/lib/color';
import {LightProvider} from '../../../kurz-style/engine/src/lib/light';
import {CameraProvider, Plane} from '../../../kurz-style/engine/src/depth/Planes';
import {Bokeh, Bubbles, Caustics, Emitter, GradientField, LightLayer, Rays, SurfaceBand} from '../../../kurz-style/engine/src/depth/Atmosphere';
import {Anemone, Seabed} from '../../../kurz-style/engine/src/assets/Ocean';
import {Micro} from '../detail/Micro';
import {Ray, School} from '../detail/Fish';
import {Ball, Brain, Branch, FarMound, Grass, Rock, Shell, Soft, Star, Table, Tubes, Urchin, Vase, VarKelp} from '../detail/flora';
import type {Placement} from '../detail/scatter';
import {Turtle} from '../assets/Turtle';
import {isOff} from '../../../kurz-style/engine/src/lib/flags';
import {camAt, FAR_KELP, FAR_MOUNDS, FAR_REEF, FORE_KELP, FRONT_REEF, lightAt, MID_KELP, MID_REEF, RAYS, SCHOOLS_FAR, SCHOOLS_MID, SINGLES, turtlePose} from './layout';

/** the open-water (calm field) band is kept to a narrow value range so it reads as ONE calm mass, as in KB */
const OPEN_HI = mixOk(c('tide-3'), c('tide-2'), 0.78);
const OPEN_LO = mixOk(c('tide-2'), c('tide-1'), 0.3);

const CORAL_TINTS = ['coral-3', 'amber-3', 'kelp-3', 'coral-4', 'amber-4', 'tide-2'];
const ROCK_TINTS = ['ochre-1', 'ochre-2', 'coral-1'];

/** placement -> generator */
const Item: React.FC<{p: Placement; t: number; lod?: 'mid' | 'far'}> = ({p, t, lod = 'mid'}) => {
	const tintPick = (arr: string[]) => arr[Math.floor(p.variant * arr.length) % arr.length];
	switch (p.kind) {
		case 'rock':
			return <Rock seed={p.seed} x={p.x} y={p.y} rx={p.size} ry={p.size * (0.5 + p.variant * 0.25)} lod={lod} base={tintPick(ROCK_TINTS) === 'coral-1' ? 'coral-1' : undefined} />;
		case 'brain':
			return <Brain seed={p.seed} x={p.x} y={p.y} r={p.size} lod={lod} base={tintPick(['kelp-3', 'ochre-3', 'amber-3', 'coral-3'])} />;
		case 'vase':
			return <Vase seed={p.seed} x={p.x} y={p.y} h={p.size} lod={lod} base={tintPick(['ochre-2', 'coral-2', 'amber-2', 'tide-1'])} />;
		case 'table':
			return <Table seed={p.seed} x={p.x} y={p.y} w={p.size} lod={lod} base={tintPick(['amber-3', 'kelp-3', 'ochre-3'])} />;
		case 'branch':
			return <Branch seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={tintPick(CORAL_TINTS)} />;
		case 'tubes':
			return <Tubes seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={tintPick(['coral-2', 'amber-3', 'tide-2', 'kelp-2'])} />;
		case 'ball':
			return <Ball seed={p.seed} x={p.x} y={p.y} r={p.size} lod={lod} base={tintPick(['amber-4', 'coral-3', 'ochre-3'])} />;
		case 'soft':
			return <Soft seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} base={tintPick(['coral-4', 'amber-4', 'kelp-4', 'tide-3'])} />;
		case 'grass':
			return <Grass seed={p.seed} x={p.x} y={p.y} h={p.size} t={t} lod={lod} />;
		case 'urchin':
			return <Urchin seed={p.seed} x={p.x} y={p.y} r={p.size} t={t} />;
		case 'star':
			return <Star seed={p.seed} x={p.x} y={p.y} s={p.size} base={tintPick(['coral-3', 'amber-4', 'coral-4'])} />;
		case 'shell':
			return <Shell seed={p.seed} x={p.x} y={p.y} s={p.size} />;
		case 'anemone':
			return <Anemone x={p.x} y={p.y} s={p.size} t={t} seed={p.seed} />;
		default:
			return null;
	}
};

export const DetailShowcase: React.FC = () => {
	const frame = useCurrentFrame();
	const {fps} = useVideoConfig();
	const t = frame / fps;
	const light = lightAt(t);
	const ref = lightAt(0);
	const cam = camAt(t);
	const tp = turtlePose(t);
	const sunX = 540 + Math.cos(Math.atan2(light.key[1], light.key[0])) * 900;

	return (
		<LightProvider light={light}>
			<CameraProvider cam={cam}>
				<AbsoluteFill style={{backgroundColor: c('tide-1')}}>
					{/* P0 field */}
					<Plane preset="field">
						<GradientField
							id="sea"
							stops={[
								[0, 'tide-4'],
								[0.1, 'tide-3'],
								[0.2, OPEN_HI],
								[0.62, OPEN_LO],
								[0.8, 'tide-1'],
								[1, 'tide-0'],
							]}
							glow={{x: sunX, y: 60, r: 1000, color: 'tide-5', a: 0.3}}
						/>
						<SurfaceBand t={t} y={-150} color="tide-5" />
						<LightLayer>
							<Caustics t={t} seed="surf" area={[-260, -260, 1600, 560]} cell={80} color="tide-5" alpha={0.12} width={3.2} />
							<Rays t={t} seed="sun" x={sunX} y={-40} n={7} angle={72} spread={44} len={2500} alpha={0.085} />
							<Emitter id="sun" x={sunX} y={-110} r={56} t={t} ramp={['bone-2', 'amber-5', 'amber-4']} halo="amber-5" haloScale={1.3} sparkles={6} />
						</LightLayer>
					</Plane>

					{/* P1 far */}
					<Plane preset="far">
						{FAR_MOUNDS.map((m) => (
							<FarMound key={m.seed} {...m} />
						))}
						{FAR_KELP.map((k) => (
							<VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style={k.style} lod="far" />
						))}
						{isOff('far') ? null : FAR_REEF.map((p) => (
							<Item key={p.id} p={p} t={t} lod="far" />
						))}
						{isOff('farfish') ? null : SCHOOLS_FAR.map((s) => (
							<School key={s.id} spec={s} t={t} />
						))}
						{RAYS.map((r) => (
							<Ray key={r.seed} {...r} t={t} color="tide-0" />
						))}
						{isOff('micro') ? null : <Micro t={t} seed="mfar" preset="far" />}
					</Plane>

					{/* P1.5 back: the kelp groves, between far and mid (haze step 0.42) */}
					<Plane preset="mid" spec={{depth: 0.45, haze: 0.42, desat: 0.06}}>
						{isOff('kelp') ? null : MID_KELP.map((k) => (
							<VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style={k.style} />
						))}
					</Plane>

					{/* P2 mid */}
					<Plane preset="mid" spec={{haze: 0.3, desat: 0.05}}>
						{isOff('seabed') ? null : <Seabed y={1470} t={t} seed="bed" />}
						<LightLayer opacity={0.9}>
							<Caustics t={t} seed="sand" area={[-260, 1480, 1600, 600]} cell={58} color="amber-5" alpha={0.08} width={2.6} fadeDown={false} />
						</LightLayer>
						{isOff('midreef') ? null : MID_REEF.map((p) => (
							<Item key={p.id} p={p} t={t} />
						))}
						{isOff('schools') ? null : SCHOOLS_MID.map((s) => (
							<School key={s.id} spec={s} t={t} />
						))}
						{isOff('micro') ? null : <Micro t={t} seed="mmid" preset="mid" />}
					</Plane>

					{/* P3 subject */}
					<Plane preset="subject">
						{isOff('turtle') ? null : (
							<g transform={`translate(${tp.x.toFixed(1)} ${tp.y.toFixed(1)}) rotate(${tp.rot.toFixed(2)} 300 215) scale(${tp.s})`}>
								<Turtle t={t} rot={tp.rot} refKey={ref.key} refRim={ref.rim} />
							</g>
						)}
						{isOff('front') ? null : FRONT_REEF.map((p) => (
							<Item key={p.id} p={p} t={t} />
						))}
						{isOff('singles') ? null : SINGLES.map((s) => (
							<School key={s.id} spec={s} t={t} />
						))}
						<Bubbles t={t} seed="vent" x={640} y={1790} n={10} rate={2.6} rise={80} size={[3, 9]} />
						{isOff('micro') ? null : <Micro t={t} seed="mnear" preset="near" />}
					</Plane>

					{/* P4 fore */}
					<Plane preset="fore" spec={{blur: 5}}>
						{isOff('fore') ? null : FORE_KELP.map((k) => (
							<VarKelp key={k.id} seed={k.seed} x={k.x} y={k.y} h={k.h} t={t} lean={k.lean} bend={k.bend} style="broad" silhouette />
						))}
						<Branch seed="fgb" x={-40} y={2090} h={420} t={t} base="ink-1" lod="far" />
						<Soft seed="fgs" x={1120} y={2080} h={260} t={t} base="ink-1" lod="far" />
						<Bokeh t={t} seed="bk" n={10} r={[14, 40]} />
					</Plane>

					<AbsoluteFill style={{background: `radial-gradient(ellipse 85% 65% at 50% 45%, ${rgba(c('ink-0'), 0)} 62%, ${rgba(c('ink-0'), 0.38)} 100%)`}} />
				</AbsoluteFill>
			</CameraProvider>
		</LightProvider>
	);
};
